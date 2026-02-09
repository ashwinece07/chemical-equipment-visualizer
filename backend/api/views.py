import pandas as pd
import numpy as np
import os
import io
import json
import google.generativeai as genai
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- DJANGO IMPORTS ---
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# --- APP IMPORTS ---
from .models import UploadedDataset, UserProfile
from .serializers import UploadedDatasetSerializer, UserSerializer, ChangePasswordSerializer

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyColl9KbQNAr-NR0xA59UZRJ0abafXKci0"
genai.configure(api_key=GEMINI_API_KEY)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# --- HELPER FUNCTION FOR ANALYSIS ---
def analyze_dataframe(df):
    """Enhanced analysis with trend detection and better statistics"""
    # 1. Smart Column Detection
    def get_col(candidates):
        for col in df.columns:
            if col.lower() in [c.lower() for c in candidates]: return col
        return None

    col_type = get_col(['Type', 'Equipment Type', 'Category', 'Equipment_Type'])
    col_flow = get_col(['Flowrate', 'Flow', 'Flow Rate', 'Flow_Rate'])
    col_press = get_col(['Pressure', 'Press', 'Bar'])
    col_temp = get_col(['Temperature', 'Temp', 'Deg C', 'DegC'])
    col_name = get_col(['Equipment_Name', 'Name', 'Equipment Name', 'Equipment'])
    col_timestamp = get_col(['Timestamp', 'Date', 'Time', 'DateTime'])

    # 2. Cleaning Data
    numeric_cols = []
    if col_flow: numeric_cols.append(col_flow)
    if col_press: numeric_cols.append(col_press)
    if col_temp: numeric_cols.append(col_temp)

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=numeric_cols)

    # 3. Calculate Correlation
    correlation = {}
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        for i, row in enumerate(corr_matrix.index):
            for j, col in enumerate(corr_matrix.columns):
                if i < j:
                    correlation[f"{row} vs {col}"] = round(corr_matrix.loc[row, col], 2)

    # 4. Health Score Algorithm (Enhanced)
    health_scores = []
    for index, row in df.iterrows():
        score = 100
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                z = abs((row[col] - mean) / std)
                if z > 3: score -= 30
                elif z > 2: score -= 20
                elif z > 1: score -= 10
        health_scores.append(max(0, score))
    
    df['Health_Score'] = health_scores

    # 5. Outlier Detection
    outliers = 0
    outlier_details = []
    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        outlier_mask = z_scores > 3
        outliers += np.sum(outlier_mask)
        if np.sum(outlier_mask) > 0:
            outlier_details.append({
                'parameter': col,
                'count': int(np.sum(outlier_mask)),
                'percentage': round(np.sum(outlier_mask) / len(df) * 100, 2)
            })

    # 6. Statistical Summary
    statistics = {}
    for col in numeric_cols:
        statistics[col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'q25': float(df[col].quantile(0.25)),
            'q75': float(df[col].quantile(0.75))
        }

    # 7. Trend Analysis (if timestamp exists)
    trends = {}
    if col_timestamp:
        try:
            df[col_timestamp] = pd.to_datetime(df[col_timestamp], errors='coerce')
            df = df.dropna(subset=[col_timestamp])
            df = df.sort_values(col_timestamp)
            
            for col in numeric_cols:
                # Simple linear regression for trend
                x = np.arange(len(df))
                y = df[col].values
                slope, intercept = np.polyfit(x, y, 1)
                trends[col] = {
                    'direction': 'increasing' if slope > 0 else 'decreasing',
                    'slope': float(slope),
                    'change_rate': float(slope / df[col].mean() * 100) if df[col].mean() != 0 else 0
                }
        except:
            pass

    # 8. Equipment Type Analysis
    type_stats = {}
    if col_type:
        for eq_type in df[col_type].unique():
            type_df = df[df[col_type] == eq_type]
            type_stats[eq_type] = {
                'count': int(len(type_df)),
                'avg_health': float(type_df['Health_Score'].mean()),
                'avg_pressure': float(type_df[col_press].mean()) if col_press else 0,
                'avg_temp': float(type_df[col_temp].mean()) if col_temp else 0
            }

    # 9. Enhanced AI Analysis with Better Prompting
    ai_summary = "AI Insights unavailable."
    try:
        model = genai.GenerativeModel(
            'gemini-1.5-flash-latest',
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            )
        )
        
        # Build detailed equipment breakdown
        equipment_types = df[col_type].value_counts().to_dict() if col_type else {}
        equipment_breakdown = "\n".join([f"  • {k}: {v} units ({v/len(df)*100:.1f}%)" for k, v in list(equipment_types.items())[:10]])
        
        # Identify critical equipment
        critical_equipment = df[df['Health_Score'] < 50]
        critical_list = ""
        if len(critical_equipment) > 0:
            critical_list = "\n".join([f"  • {row.get(col_name, 'Unknown')}: Health {row['Health_Score']:.0f}%" 
                                      for _, row in critical_equipment.head(5).iterrows()])
        
        # Parameter ranges and deviations
        param_analysis = ""
        for col in numeric_cols:
            cv = (df[col].std() / df[col].mean() * 100) if df[col].mean() != 0 else 0
            param_analysis += f"\n  • {col}: Mean={df[col].mean():.2f}, StdDev={df[col].std():.2f}, CV={cv:.1f}%"
        
        # Correlation insights
        strong_correlations = {k: v for k, v in correlation.items() if abs(v) > 0.7}
        corr_text = "\n".join([f"  • {k}: {v:.2f}" for k, v in strong_correlations.items()]) if strong_correlations else "  • No strong correlations detected"
        
        separator = "=" * 63
        
        prompt = f"""As a senior chemical process engineer with 20+ years of experience, analyze this industrial equipment dataset and provide actionable insights.

{separator}
DATASET OVERVIEW
{separator}
Total Equipment Analyzed: {len(df)} units
Equipment Categories:
{equipment_breakdown}

{separator}
OPERATIONAL PARAMETERS
{separator}
{param_analysis}

Overall System Health: {np.mean(health_scores):.1f}%

{separator}
ANOMALY & RISK INDICATORS
{separator}
Statistical Outliers Detected: {outliers} data points (Z-score > 3 sigma)
Equipment Below Optimal Performance (<70%): {len([s for s in health_scores if s < 70])} units
Critical Equipment Requiring Immediate Attention (<50%): {len([s for s in health_scores if s < 50])} units

{f"Critical Equipment List: {critical_list}" if critical_list else ""}

{separator}
CORRELATION ANALYSIS
{separator}
Strong Correlations (|r| > 0.7):
{corr_text}

{separator}
REQUIRED ANALYSIS OUTPUT
{separator}

Provide a comprehensive professional analysis in the following structure:

EXECUTIVE SUMMARY
Provide 3-4 sentences covering overall system health status, most critical finding requiring immediate action, primary operational concern, and overall risk level.

KEY FINDINGS
Provide 5-6 specific data-driven findings about equipment performance patterns, parameter relationships, efficiency observations, unusual patterns, and comparative analysis.

RISK ASSESSMENT
Identify 4-5 specific risks including equipment failure risks, safety concerns, process efficiency risks, maintenance-related risks, and operational continuity threats.

ACTIONABLE RECOMMENDATIONS
Provide 6-8 prioritized recommendations organized by timeline: IMMEDIATE (24-48 hours), SHORT-TERM (1-2 weeks), MEDIUM-TERM (1-3 months), and LONG-TERM (3-6 months). Be specific with equipment types, target parameter ranges, expected impact, and monitoring frequency.

TECHNICAL INSIGHTS
Provide 3-4 deeper technical observations about process optimization, energy efficiency, equipment lifecycle, and predictive maintenance.

Use professional engineering terminology. Be specific with numbers and thresholds. Format with clear sections and bullet points."""
        
        response = model.generate_content(prompt)
        ai_summary = response.text
        
    except Exception as e:
        print(f"AI Error: {e}") 
        import traceback
        traceback.print_exc()
        
        # Enhanced fallback analysis
        critical_count = len([s for s in health_scores if s < 50])
        warning_count = len([s for s in health_scores if 50 <= s < 70])
        equipment_types = df[col_type].value_counts().to_dict() if col_type else {}
        
        action_msg = 'Immediate action is required for critical equipment.' if critical_count > 0 else 'System is operating within acceptable parameters.'
        variability_level = 'High' if any((df[col].std() / df[col].mean() * 100) > 20 for col in numeric_cols if df[col].mean() != 0) else 'Moderate'
        risk_level = 'HIGH' if critical_count > 0 else 'MEDIUM' if warning_count > 3 else 'LOW'
        data_quality = 'Sensor calibration recommended' if outliers > len(df) * 0.05 else 'Data quality is acceptable'
        reliability = 'excellent' if np.mean(health_scores) >= 85 else 'good' if np.mean(health_scores) >= 70 else 'concerning'
        
        ai_summary = f"""## EXECUTIVE SUMMARY

The system comprises {len(df)} equipment units with an overall health score of {np.mean(health_scores):.1f}%. Analysis reveals {outliers} statistical outliers and {critical_count + warning_count} units requiring attention. {action_msg}

## KEY FINDINGS

• Equipment Distribution: {len(equipment_types)} equipment categories analyzed
• Health Status: {len([s for s in health_scores if s >= 90])} excellent, {len([s for s in health_scores if 70 <= s < 90])} good, {warning_count} fair, {critical_count} poor
• Parameter Ranges:
  - Pressure: {df[col_press].min() if col_press else 0:.2f} - {df[col_press].max() if col_press else 0:.2f} bar (avg: {df[col_press].mean() if col_press else 0:.2f})
  - Temperature: {df[col_temp].min() if col_temp else 0:.2f} - {df[col_temp].max() if col_temp else 0:.2f} C (avg: {df[col_temp].mean() if col_temp else 0:.2f})
  - Flowrate: {df[col_flow].min() if col_flow else 0:.2f} - {df[col_flow].max() if col_flow else 0:.2f} (avg: {df[col_flow].mean() if col_flow else 0:.2f})
• Outlier Detection: {outliers} data points exceed 3-sigma threshold
• Variability: {variability_level} parameter variability detected

## RISK ASSESSMENT

• Critical Equipment Risk: {critical_count} units below 50% health score require immediate inspection
• Performance Degradation: {warning_count} units showing early signs of performance issues
• Statistical Anomalies: {outliers} outlier data points may indicate sensor issues or process upsets
• Operational Risk Level: {risk_level}

## ACTIONABLE RECOMMENDATIONS

IMMEDIATE (24-48 hours):
1. Inspect {critical_count} critical equipment units with health scores below 50%
2. Verify sensor calibration for equipment showing outlier readings
3. Review operating procedures for equipment with high parameter variability

SHORT-TERM (1-2 weeks):
4. Implement enhanced monitoring for {warning_count} equipment units in fair condition
5. Conduct preventive maintenance on equipment approaching lower health thresholds
6. Analyze correlation patterns to optimize process parameters

MEDIUM-TERM (1-3 months):
7. Develop predictive maintenance schedule based on health score trends
8. Standardize operating parameters to reduce variability
9. Implement automated alerting for equipment health degradation

LONG-TERM (3-6 months):
10. Consider equipment upgrades for consistently underperforming units
11. Establish baseline performance metrics for all equipment categories
12. Implement continuous monitoring and data analytics platform

## TECHNICAL INSIGHTS

• Process Optimization: Parameter correlations suggest opportunities for efficiency improvements
• Maintenance Strategy: Health score distribution indicates need for condition-based maintenance
• Data Quality: {data_quality}
• System Reliability: Overall health score of {np.mean(health_scores):.1f}% indicates {reliability} system reliability

---
Note: AI analysis temporarily unavailable. This is an automated statistical summary."""

    return {
        "total_count": int(len(df)),
        "outliers_count": int(outliers),
        "outlier_details": outlier_details,
        "health_score_avg": float(np.mean(health_scores)),
        "health_score_distribution": {
            'excellent': int(len([s for s in health_scores if s >= 90])),
            'good': int(len([s for s in health_scores if 70 <= s < 90])),
            'fair': int(len([s for s in health_scores if 50 <= s < 70])),
            'poor': int(len([s for s in health_scores if s < 50]))
        },
        "type_distribution": df[col_type].value_counts().to_dict() if col_type else {},
        "type_statistics": type_stats,
        "correlation": correlation,
        "statistics": statistics,
        "trends": trends,
        "ai_insights": ai_summary,
        "averages": {
            "Flowrate": float(df[col_flow].mean()) if col_flow else 0,
            "Pressure": float(df[col_press].mean()) if col_press else 0,
            "Temperature": float(df[col_temp].mean()) if col_temp else 0
        },
        "raw_data": df.head(20).fillna("").to_dict(orient='records'),
        "full_df": df,
        "column_names": {
            'type': col_type,
            'flow': col_flow,
            'pressure': col_press,
            'temperature': col_temp,
            'name': col_name,
            'timestamp': col_timestamp
        }
    }

# --- AUTHENTICATION VIEWS ---
class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT Login with user info"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data.get('username'))
            response.data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        return response

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

# --- USER PROFILE VIEWS ---
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        upload_count = UploadedDataset.objects.filter(user=request.user).count()
        total_size = sum([d.file_size for d in UploadedDataset.objects.filter(user=request.user)])
        
        data = serializer.data
        data['upload_count'] = upload_count
        data['total_storage'] = total_size
        data['storage_mb'] = round(total_size / (1024 * 1024), 2)
        return Response(data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)
            
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- FILE UPLOAD & ANALYSIS VIEWS ---
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        # Validate file size
        if file_obj.size > MAX_FILE_SIZE:
            return Response({"error": f"File size exceeds 10MB limit. Your file: {file_obj.size / (1024*1024):.2f}MB"}, status=400)

        # Validate file type
        if not file_obj.name.endswith('.csv'):
            return Response({"error": "Only CSV files are allowed"}, status=400)

        dataset = UploadedDataset.objects.create(user=request.user, file=file_obj)

        # Cleanup: Keep only last 10 files
        user_files = UploadedDataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if user_files.count() > 10:
            for f in user_files[10:]:
                if f.file and os.path.isfile(f.file.path):
                    os.remove(f.file.path)
                f.delete()

        try:
            # Read CSV
            try:
                df = pd.read_csv(dataset.file.path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(dataset.file.path, encoding='latin1')
            
            df.columns = df.columns.str.strip()
            
            # Update row count
            dataset.row_count = len(df)
            dataset.save()
            
            # Analyze
            stats = analyze_dataframe(df)
            
            # Remove full_df before sending (too large)
            stats.pop('full_df', None)
            
            return Response({"status": "success", "data": stats, "file_id": dataset.id})
        except Exception as e:
            dataset.delete()
            return Response({"error": f"Processing Error: {str(e)}"}, status=500)

class AnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            dataset = UploadedDataset.objects.get(id=file_id, user=request.user)
            try:
                df = pd.read_csv(dataset.file.path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(dataset.file.path, encoding='latin1')
            
            df.columns = df.columns.str.strip()
            stats = analyze_dataframe(df)
            stats.pop('full_df', None)
            
            return Response({"status": "success", "data": stats, "file_id": dataset.id})
        except UploadedDataset.DoesNotExist:
            return Response({"error": "File not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CompareDatasetView(APIView):
    """Compare two datasets side by side"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_id_1 = request.data.get('file_id_1')
        file_id_2 = request.data.get('file_id_2')

        if not file_id_1 or not file_id_2:
            return Response({"error": "Two file IDs required"}, status=400)

        try:
            dataset1 = UploadedDataset.objects.get(id=file_id_1, user=request.user)
            dataset2 = UploadedDataset.objects.get(id=file_id_2, user=request.user)

            df1 = pd.read_csv(dataset1.file.path, encoding='utf-8-sig')
            df2 = pd.read_csv(dataset2.file.path, encoding='utf-8-sig')

            stats1 = analyze_dataframe(df1)
            stats2 = analyze_dataframe(df2)

            stats1.pop('full_df', None)
            stats2.pop('full_df', None)

            return Response({
                "dataset1": {"name": dataset1.filename, "stats": stats1},
                "dataset2": {"name": dataset2.filename, "stats": stats2}
            })
        except UploadedDataset.DoesNotExist:
            return Response({"error": "One or both files not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# --- EXPORT VIEWS (Enhanced) ---
class ExportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, file_id):
        try:
            dataset = UploadedDataset.objects.get(id=file_id, user=request.user)
            user_password = request.data.get('password')
            if not user_password:
                return Response({"error": "Password required for encryption"}, status=400)

            try:
                df = pd.read_csv(dataset.file.path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(dataset.file.path, encoding='latin1')
            df.columns = df.columns.str.strip()
            stats = analyze_dataframe(df)

            buffer = io.BytesIO()
            encrypt = StandardEncryption(user_password, canPrint=1, canCopy=0, canModify=0)
            
            doc = SimpleDocTemplate(buffer, pagesize=letter, encrypt=encrypt,
                                   topMargin=0.5*inch, bottomMargin=0.5*inch,
                                   leftMargin=0.75*inch, rightMargin=0.75*inch)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom Styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=28,
                textColor=colors.HexColor('#1e3a8a'),
                spaceAfter=10,
                alignment=1,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#64748b'),
                spaceAfter=30,
                alignment=1
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#1e40af'),
                spaceBefore=20,
                spaceAfter=12,
                fontName='Helvetica-Bold',
                borderWidth=0,
                borderColor=colors.HexColor('#3b82f6'),
                borderPadding=5
            )
            
            # Cover Page
            story.append(Spacer(1, 1.5*inch))
            story.append(Paragraph("CHEMICAL EQUIPMENT", title_style))
            story.append(Paragraph("ANALYSIS REPORT", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            file_date = dataset.uploaded_at.strftime('%B %d, %Y at %H:%M')
            story.append(Paragraph(f"Generated: {file_date}", subtitle_style))
            story.append(Paragraph(f"Dataset: {dataset.filename}", subtitle_style))
            story.append(Paragraph(f"Total Records: {stats['total_count']} equipment units", subtitle_style))
            
            # Horizontal line
            story.append(Spacer(1, 0.5*inch))
            story.append(PageBreak())
            
            # Executive Summary
            story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
            summary_text = f"""This report presents a comprehensive analysis of {stats['total_count']} equipment units 
across {len(stats['type_distribution'])} categories. The overall system health score is {stats['health_score_avg']:.1f}%, 
with {stats['outliers_count']} statistical outliers detected requiring immediate attention."""
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Key Metrics Dashboard
            story.append(Paragraph("KEY PERFORMANCE INDICATORS", heading_style))
            
            kpi_data = [
                ['Metric', 'Value', 'Status'],
                ['Total Equipment Units', str(stats['total_count']), '✓'],
                ['Average Health Score', f"{stats['health_score_avg']:.1f}%", 
                 '✓' if stats['health_score_avg'] >= 80 else '⚠'],
                ['Statistical Outliers', str(stats['outliers_count']), 
                 '✓' if stats['outliers_count'] < 5 else '⚠'],
                ['Avg Pressure', f"{stats['averages']['Pressure']:.2f} bar", '✓'],
                ['Avg Temperature', f"{stats['averages']['Temperature']:.2f} °C", '✓'],
                ['Avg Flowrate', f"{stats['averages']['Flowrate']:.2f}", '✓'],
            ]
            
            kpi_table = Table(kpi_data, colWidths=[2.5*inch, 2*inch, 1*inch])
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            story.append(kpi_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Health Score Distribution
            story.append(Paragraph("HEALTH SCORE DISTRIBUTION", heading_style))
            health_dist = stats.get('health_score_distribution', {})
            health_data = [
                ['Category', 'Count', 'Percentage'],
                ['Excellent (90-100%)', str(health_dist.get('excellent', 0)), 
                 f"{health_dist.get('excellent', 0)/stats['total_count']*100:.1f}%"],
                ['Good (70-89%)', str(health_dist.get('good', 0)), 
                 f"{health_dist.get('good', 0)/stats['total_count']*100:.1f}%"],
                ['Fair (50-69%)', str(health_dist.get('fair', 0)), 
                 f"{health_dist.get('fair', 0)/stats['total_count']*100:.1f}%"],
                ['Poor (<50%)', str(health_dist.get('poor', 0)), 
                 f"{health_dist.get('poor', 0)/stats['total_count']*100:.1f}%"],
            ]
            
            health_table = Table(health_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            health_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')])
            ]))
            story.append(health_table)
            story.append(PageBreak())
            
            # AI Insights
            story.append(Paragraph("AI-POWERED ANALYSIS", heading_style))
            ai_paragraphs = stats['ai_insights'].split('\n\n')
            for para in ai_paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
            story.append(PageBreak())
            
            # Equipment Type Distribution
            if stats['type_distribution']:
                story.append(Paragraph("EQUIPMENT TYPE BREAKDOWN", heading_style))
                type_data = [['Equipment Type', 'Count', 'Percentage']]
                total = sum(stats['type_distribution'].values())
                for eq_type, count in stats['type_distribution'].items():
                    percentage = (count / total * 100)
                    type_data.append([str(eq_type), str(count), f"{percentage:.1f}%"])
                
                type_table = Table(type_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
                type_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')])
                ]))
                story.append(type_table)
            
            # Footer
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#94a3b8'),
                alignment=1
            )
            story.append(Paragraph("This report is password-protected and confidential.", footer_style))
            story.append(Paragraph(f"Generated by Chemical Equipment Visualizer | {file_date}", footer_style))
            
            doc.build(story)
            buffer.seek(0)
            
            response = HttpResponse(buffer, content_type='application/pdf')
            filename_base = dataset.filename.replace('.csv', '')
            response['Content-Disposition'] = f'attachment; filename="{filename_base}_Professional_Report.pdf"'
            return response

        except Exception as e:
            print(f"PDF Error: {e}")
            return Response({"error": str(e)}, status=500)

class ExportExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, file_id):
        try:
            dataset = UploadedDataset.objects.get(id=file_id, user=request.user)
            user_password = request.data.get('password')
            if not user_password:
                return Response({"error": "Password required for encryption"}, status=400)

            try:
                df = pd.read_csv(dataset.file.path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(dataset.file.path, encoding='latin1')
            
            df.columns = df.columns.str.strip()
            stats = analyze_dataframe(df)
            
            import xlsxwriter
            
            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer, {'in_memory': True})
            
            # Sheet 1: Raw Data
            ws1 = workbook.add_worksheet('Raw Data')
            for col_num, col_name in enumerate(df.columns):
                ws1.write(0, col_num, col_name)
            for row_num, row_data in enumerate(df.values, start=1):
                for col_num, cell_data in enumerate(row_data):
                    ws1.write(row_num, col_num, str(cell_data))
            
            # Sheet 2: Summary
            ws2 = workbook.add_worksheet('Summary')
            ws2.write(0, 0, 'Metric')
            ws2.write(0, 1, 'Value')
            ws2.write(1, 0, 'Total Equipment')
            ws2.write(1, 1, stats['total_count'])
            ws2.write(2, 0, 'Avg Health Score')
            ws2.write(2, 1, f"{stats['health_score_avg']:.1f}%")
            ws2.write(3, 0, 'Outliers')
            ws2.write(3, 1, stats['outliers_count'])
            ws2.write(4, 0, 'Avg Pressure')
            ws2.write(4, 1, f"{stats['averages']['Pressure']:.2f}")
            ws2.write(5, 0, 'Avg Temperature')
            ws2.write(5, 1, f"{stats['averages']['Temperature']:.2f}")
            ws2.write(6, 0, 'Avg Flowrate')
            ws2.write(6, 1, f"{stats['averages']['Flowrate']:.2f}")
            
            # Sheet 3: Equipment Types
            if stats['type_distribution']:
                ws3 = workbook.add_worksheet('Equipment Types')
                ws3.write(0, 0, 'Type')
                ws3.write(0, 1, 'Count')
                row = 1
                for eq_type, count in stats['type_distribution'].items():
                    ws3.write(row, 0, str(eq_type))
                    ws3.write(row, 1, count)
                    row += 1
            
            # Sheet 4: AI Insights
            ws4 = workbook.add_worksheet('AI Insights')
            ws4.write(0, 0, 'AI Analysis')
            ws4.write(1, 0, stats['ai_insights'])
            
            # Sheet 5: Health Distribution
            health_dist = stats.get('health_score_distribution', {})
            ws5 = workbook.add_worksheet('Health Distribution')
            ws5.write(0, 0, 'Category')
            ws5.write(0, 1, 'Count')
            ws5.write(1, 0, 'Excellent (90-100%)')
            ws5.write(1, 1, health_dist.get('excellent', 0))
            ws5.write(2, 0, 'Good (70-89%)')
            ws5.write(2, 1, health_dist.get('good', 0))
            ws5.write(3, 0, 'Fair (50-69%)')
            ws5.write(3, 1, health_dist.get('fair', 0))
            ws5.write(4, 0, 'Poor (<50%)')
            ws5.write(4, 1, health_dist.get('poor', 0))
            
            # Sheet 6: Correlations
            if stats['correlation']:
                ws6 = workbook.add_worksheet('Correlations')
                ws6.write(0, 0, 'Parameters')
                ws6.write(0, 1, 'Correlation')
                row = 1
                for params, corr in stats['correlation'].items():
                    ws6.write(row, 0, params)
                    ws6.write(row, 1, corr)
                    row += 1
            
            # Protect workbook with password
            workbook.set_properties({
                'title': 'Chemical Equipment Analysis',
                'subject': 'Professional Analysis Report',
                'author': 'Chemical Visualizer',
                'comments': 'Password Protected Report'
            })
            
            # Protect each sheet
            for worksheet in workbook.worksheets():
                worksheet.protect(user_password, {'objects': True, 'scenarios': True})
            
            workbook.close()
            excel_data = buffer.getvalue()
            
            original_name = dataset.filename
            if original_name.lower().endswith('.csv'):
                base_name = original_name[:-4]
            else:
                base_name = original_name
                
            final_filename = f"{base_name}_Professional_Analysis.xlsx"

            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{final_filename}"'
            response['Content-Length'] = len(excel_data)
            return response

        except Exception as e:
            print(f"Excel Export Error: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

# --- HISTORY & DELETE VIEWS ---
class DeleteDatasetView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, file_id):
        try:
            dataset = UploadedDataset.objects.get(id=file_id, user=request.user)
            if dataset.file and os.path.isfile(dataset.file.path):
                os.remove(dataset.file.path)
            dataset.delete()
            return Response({"status": "deleted"})
        except UploadedDataset.DoesNotExist:
            return Response({"error": "File not found"}, status=404)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = UploadedDataset.objects.filter(user=request.user).order_by('-uploaded_at')[:10]
        serializer = UploadedDatasetSerializer(datasets, many=True)
        return Response(serializer.data)

# Legacy Token Auth (for backward compatibility)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
