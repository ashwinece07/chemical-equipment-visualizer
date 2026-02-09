import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { getUserProfile, updateUserProfile, changePassword, logoutUser } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import { User, Mail, Lock, Save, LogOut, Database, Calendar, Building, Phone } from 'lucide-react';
import { motion } from 'framer-motion';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    profile: {
      company: '',
      phone: '',
      bio: ''
    }
  });
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getUserProfile();
      setProfile(data);
      setFormData({
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        email: data.email || '',
        profile: {
          company: data.profile?.company || '',
          phone: data.profile?.phone || '',
          bio: data.profile?.bio || ''
        }
      });
    } catch (error) {
      console.error(error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const toastId = toast.loading('Updating profile...');
    try {
      await updateUserProfile(formData);
      await loadProfile();
      setEditing(false);
      toast.success('Profile updated successfully!', { id: toastId });
    } catch (error) {
      toast.error('Failed to update profile', { id: toastId });
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    
    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error('New passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    const toastId = toast.loading('Changing password...');
    try {
      await changePassword(passwordData.old_password, passwordData.new_password);
      setPasswordData({ old_password: '', new_password: '', confirm_password: '' });
      setShowPasswordForm(false);
      toast.success('Password changed successfully!', { id: toastId });
    } catch (error) {
      const errorMsg = error.response?.data?.old_password?.[0] || 'Failed to change password';
      toast.error(errorMsg, { id: toastId });
    }
  };

  const handleLogout = async () => {
    if (window.confirm('Are you sure you want to logout?')) {
      await logoutUser();
      navigate('/login');
    }
  };

  if (!profile) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
        <Navbar />
        <div className="flex items-center justify-center h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <Navbar />
      <Toaster position="bottom-right" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto px-4 py-8"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white mb-8 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">My Profile</h1>
              <p className="text-blue-100">Manage your account settings and preferences</p>
            </div>
            <div className="bg-white/20 p-4 rounded-full">
              <User size={48} />
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard 
            icon={<Database />} 
            label="Uploads" 
            value={profile.upload_count || 0}
            color="blue"
          />
          <StatCard 
            icon={<Database />} 
            label="Storage Used" 
            value={`${profile.storage_mb || 0} MB`}
            color="green"
          />
          <StatCard 
            icon={<Calendar />} 
            label="Member Since" 
            value={new Date(profile.date_joined).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
            color="purple"
          />
        </div>

        {/* Profile Information */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Profile Information</h2>
            <button
              onClick={() => setEditing(!editing)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              {editing ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>

          {editing ? (
            <form onSubmit={handleUpdateProfile} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <InputField
                  label="First Name"
                  icon={<User size={18} />}
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                />
                <InputField
                  label="Last Name"
                  icon={<User size={18} />}
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                />
              </div>

              <InputField
                label="Email"
                type="email"
                icon={<Mail size={18} />}
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />

              <InputField
                label="Company"
                icon={<Building size={18} />}
                value={formData.profile.company}
                onChange={(e) => setFormData({ 
                  ...formData, 
                  profile: { ...formData.profile, company: e.target.value }
                })}
              />

              <InputField
                label="Phone"
                icon={<Phone size={18} />}
                value={formData.profile.phone}
                onChange={(e) => setFormData({ 
                  ...formData, 
                  profile: { ...formData.profile, phone: e.target.value }
                })}
              />

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Bio
                </label>
                <textarea
                  value={formData.profile.bio}
                  onChange={(e) => setFormData({ 
                    ...formData, 
                    profile: { ...formData.profile, bio: e.target.value }
                  })}
                  rows={4}
                  className="w-full p-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Tell us about yourself..."
                />
              </div>

              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition"
              >
                <Save size={20} /> Save Changes
              </button>
            </form>
          ) : (
            <div className="space-y-4">
              <InfoRow label="Username" value={profile.username} />
              <InfoRow label="Email" value={profile.email || 'Not set'} />
              <InfoRow label="Full Name" value={`${profile.first_name || ''} ${profile.last_name || ''}`.trim() || 'Not set'} />
              <InfoRow label="Company" value={profile.profile?.company || 'Not set'} />
              <InfoRow label="Phone" value={profile.profile?.phone || 'Not set'} />
              {profile.profile?.bio && (
                <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Bio</p>
                  <p className="text-slate-600 dark:text-slate-400">{profile.profile.bio}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Password Change */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800 mb-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-2">
                <Lock size={24} /> Security
              </h2>
              <p className="text-sm text-slate-500 mt-1">Manage your password and security settings</p>
            </div>
            <button
              onClick={() => setShowPasswordForm(!showPasswordForm)}
              className="px-4 py-2 bg-slate-800 dark:bg-slate-700 text-white rounded-lg hover:bg-slate-700 transition"
            >
              {showPasswordForm ? 'Cancel' : 'Change Password'}
            </button>
          </div>

          {showPasswordForm && (
            <form onSubmit={handleChangePassword} className="space-y-6">
              <InputField
                label="Current Password"
                type="password"
                icon={<Lock size={18} />}
                value={passwordData.old_password}
                onChange={(e) => setPasswordData({ ...passwordData, old_password: e.target.value })}
                required
              />
              <InputField
                label="New Password"
                type="password"
                icon={<Lock size={18} />}
                value={passwordData.new_password}
                onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                required
              />
              <InputField
                label="Confirm New Password"
                type="password"
                icon={<Lock size={18} />}
                value={passwordData.confirm_password}
                onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                required
              />
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition"
              >
                Update Password
              </button>
            </form>
          )}
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 bg-red-600 text-white py-3 rounded-lg font-bold hover:bg-red-700 transition"
        >
          <LogOut size={20} /> Logout
        </button>
      </motion.div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color }) => {
  const colors = {
    blue: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400',
    green: 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400',
    purple: 'bg-purple-50 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400'
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
      <div className={`inline-flex p-3 rounded-lg ${colors[color]} mb-3`}>
        {icon}
      </div>
      <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
};

const InputField = ({ label, icon, type = 'text', value, onChange, required = false }) => (
  <div>
    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
      {label}
    </label>
    <div className="relative">
      <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
        {icon}
      </div>
      <input
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        className="w-full pl-10 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
      />
    </div>
  </div>
);

const InfoRow = ({ label, value }) => (
  <div className="flex justify-between items-center py-3 border-b border-slate-200 dark:border-slate-700">
    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">{label}</span>
    <span className="text-sm font-bold text-slate-900 dark:text-slate-100">{value}</span>
  </div>
);

export default Profile;
