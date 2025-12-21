import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Activate from './pages/Activate';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Documents from './pages/Documents';
import Profile from './pages/Profile';
import GenerateQcm from './pages/GenerateQcm';
import MyQcms from './pages/MyQcms';
import QcmDetails from './pages/QcmDetails';
import MyExams from './pages/MyExams';
import ExamSessionDetails from './pages/ExamSessionDetails';
import CreateExamSession from './pages/CreateExamSession';
import ActiveExams from './pages/ActiveExams';
import TakeExam from './pages/TakeExam';
import ExamResult from './pages/ExamResult';
import ExamResults from './pages/ExamResults';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import ManagerDashboard from './pages/ManagerDashboard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/activate/:token" element={<Activate />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password/:token" element={<ResetPassword />} />
          <Route path="/admin-login" element={<AdminLogin />} />

          <Route path="/admin-dashboard" element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          } />

          <Route path="/manager-dashboard" element={
            <ProtectedRoute>
              <ManagerDashboard />
            </ProtectedRoute>
          } />

          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/generate-qcm" element={<GenerateQcm />} />
            <Route path="/my-qcms" element={<MyQcms />} />
            <Route path="/qcm/:qcmId" element={<QcmDetails />} />
            <Route path="/my-exams" element={<MyExams />} />
            <Route path="/exam-session/:sessionId" element={<ExamSessionDetails />} />
            <Route path="/exam-session/:sessionId/live" element={<ExamSessionDetails />} />
            <Route path="/create-exam/:qcmId" element={<CreateExamSession />} />
            <Route path="/active-exams" element={<ActiveExams />} />
            <Route path="/exam-results/:sessionId" element={<ExamResults />} />
          </Route>

          <Route path="/take-exam" element={
            <ProtectedRoute>
              <TakeExam />
            </ProtectedRoute>
          } />
          <Route path="/exam-result" element={
            <ProtectedRoute>
              <ExamResult />
            </ProtectedRoute>
          } />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
