import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { RequireAuth } from './auth/RequireAuth';
import LandingPage from './pages/LandingPage';
import SigilPage from './pages/SigilPage';
import GalleryPage from './pages/GalleryPage';
import ProGateModal from './components/ProGateModal';

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/sigil"
          element={
            <RequireAuth returnTo="/">
              <SigilPage />
            </RequireAuth>
          }
        />
        <Route
          path="/gallery"
          element={
            <RequireAuth returnTo="/">
              <GalleryPage />
            </RequireAuth>
          }
        />
        <Route path="*" element={<LandingPage />} />
      </Routes>
      <ProGateModal />
    </>
  );
}
