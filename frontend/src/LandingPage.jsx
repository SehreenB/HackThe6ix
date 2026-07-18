import React from 'react';
import { motion } from 'motion/react';
import { Globe, Shield, Zap, ArrowRight, ChevronDown, BarChart3 } from 'lucide-react';
import Logo from './Logo';

const LandingPage = ({ onEnter }) => {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden" style={{ fontFamily: "'Inter', sans-serif" }}>

      {/* ─── Hero ────────────────────────────────────────────────── */}
      <section className="relative h-screen flex flex-col items-center justify-center px-6 overflow-hidden">

        {/* Atmospheric Background */}
        <div className="absolute inset-0 z-0">
          <img
            src="/hero.png"
            alt="Earth from Space"
            className="w-full h-full object-cover"
            style={{ opacity: 0.85, transform: 'scale(1)', animation: 'heroZoom 40s linear infinite' }}
            onError={(e) => {
              e.target.src = "https://picsum.photos/seed/earth-space/1920/1080";
            }}
          />
          {/* Vignette: dark at top/bottom/sides, clear in the center where Earth detail lives */}
          <div
            className="absolute inset-0"
            style={{ background: 'radial-gradient(ellipse 80% 80% at 50% 50%, transparent 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0.9) 100%)' }}
          />
          {/* Extra bottom fade so headline text stays legible */}
          <div
            className="absolute inset-0"
            style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, transparent 20%, transparent 60%, rgba(0,0,0,1) 100%)' }}
          />
        </div>

        {/* Scanline overlay */}
        <div className="absolute inset-0 z-0 pointer-events-none" style={{ backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,180,255,0.01) 2px, rgba(0,180,255,0.01) 4px)' }} />

        {/* Glowing orb */}
        <div className="absolute" style={{ width: 600, height: 600, borderRadius: '50%', background: 'radial-gradient(circle, rgba(0,180,255,0.06) 0%, transparent 70%)', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', pointerEvents: 'none' }} />

        <div className="relative z-10 text-center max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="inline-flex items-center gap-2 mb-8 px-5 py-2 rounded-full border shadow-[0_0_15px_rgba(0,180,255,0.1)]"
              style={{ 
                borderColor: 'rgba(0,180,255,0.5)', 
                background: 'rgba(0,180,255,0.12)', 
                color: '#FFFFFF',
                backdropFilter: 'blur(10px)',
                WebkitBackdropFilter: 'blur(10px)'
              }}
            >
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#00B4FF', display: 'inline-block', boxShadow: '0 0 8px #00B4FF', animation: 'pulse 2s ease-in-out infinite' }} />
              <span style={{ fontSize: '0.65rem', letterSpacing: '0.25em', fontWeight: 800 }}>MISSION ACTIVE — LIBERIA HEALTH INITIATIVE</span>
            </motion.div>

            <h1
              style={{
                fontSize: 'clamp(3rem, 9vw, 7rem)',
                fontWeight: 900,
                letterSpacing: '-0.04em',
                lineHeight: 1,
                marginBottom: '1.5rem',
              }}
            >
              APOGEE
              <br />
              <span style={{ color: '#00B4FF' }}>SOLUTIONS</span>
            </h1>

            <p style={{ 
              fontSize: 'clamp(1.1rem, 2.2vw, 1.35rem)', 
              color: 'rgba(255,255,255,0.85)', 
              maxWidth: 800, 
              margin: '0 auto 3.5rem', 
              lineHeight: 1.8, 
              fontWeight: 400,
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}>
              Leveraging satellite data and advanced optimization protocols to bridge the 2-hour surgical access gap across the Liberian territory.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <motion.button
                onClick={onEnter}
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
                className="group flex items-center gap-3"
                style={{
                  background: '#fff',
                  color: '#000',
                  padding: '1.1rem 2.4rem',
                  borderRadius: 9999,
                  fontWeight: 900,
                  fontSize: '0.7rem',
                  letterSpacing: '0.18em',
                  textTransform: 'uppercase',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'background 0.2s, color 0.2s',
                }}
                onMouseEnter={e => { e.currentTarget.style.background = '#00B4FF'; e.currentTarget.style.color = '#fff'; }}
                onMouseLeave={e => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.color = '#000'; }}
              >
                Enter Mission Control
                <ArrowRight size={16} style={{ transition: 'transform 0.2s' }} className="group-hover:translate-x-1" />
              </motion.button>

              <motion.button
                onClick={() => document.getElementById('mission-objectives')?.scrollIntoView({ behavior: 'smooth' })}
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
                style={{
                  padding: '1.1rem 2.4rem',
                  borderRadius: 9999,
                  fontWeight: 700,
                  fontSize: '0.7rem',
                  letterSpacing: '0.18em',
                  textTransform: 'uppercase',
                  border: '1px solid rgba(255,255,255,0.2)',
                  background: 'transparent',
                  color: '#fff',
                  cursor: 'pointer',
                  transition: 'background 0.2s',
                }}
                onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.05)'; }}
                onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; }}
              >
                View Mission Brief
              </motion.button>
            </div>
          </motion.div>
        </div>

        {/* Scroll hint */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.6, duration: 1 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
          style={{ color: 'rgba(255,255,255,0.25)' }}
        >
          <span style={{ fontSize: '0.6rem', letterSpacing: '0.3em', textTransform: 'uppercase' }}>Scroll to Explore</span>
          <ChevronDown size={18} style={{ animation: 'bounce 1.5s ease-in-out infinite' }} />
        </motion.div>
      </section>

      {/* ─── Mission Objectives ──────────────────────────────────── */}
      <section id="mission-objectives" style={{ padding: '8rem 1.5rem', background: '#0A0E1A', position: 'relative', zIndex: 10 }}>
        <div style={{ maxWidth: 1280, margin: '0 auto' }}>
          {/* Section header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            style={{ textAlign: 'center', marginBottom: '4rem' }}
          >
            <div style={{ fontSize: '0.6rem', letterSpacing: '0.3em', textTransform: 'uppercase', color: '#00B4FF', marginBottom: '1rem' }}>Mission Objectives</div>
            <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 900, letterSpacing: '-0.03em' }}>
              THREE PILLARS OF<br />
              <span style={{ color: '#00B4FF' }}>OPERATIONAL INTEL</span>
            </h2>
          </motion.div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
            <ObjectiveCard
              index={0}
              icon={<Shield size={30} color="#FF3B5C" />}
              accentColor="#FF3B5C"
              title="Access Security"
              description="Identifying regions where population centers are more than 120 minutes away from life-saving surgical intervention."
            />
            <ObjectiveCard
              index={1}
              icon={<Zap size={30} color="#00FF88" />}
              accentColor="#00FF88"
              title="Strategic Optimization"
              description="Using proprietary algorithms to simulate the impact of new facility placements on national health security."
            />
            <ObjectiveCard
              index={2}
              icon={<BarChart3 size={30} color="#00B4FF" />}
              accentColor="#00B4FF"
              title="Data Intelligence"
              description="Real-time telemetry and regional analytics providing a comprehensive overview of the surgical landscape."
            />
          </div>
        </div>
      </section>

      {/* ─── Impact / Stats ──────────────────────────────────────── */}
      <section style={{ padding: '8rem 1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', display: 'flex', flexWrap: 'wrap', gap: '5rem', alignItems: 'center' }}>

          {/* Left copy */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            style={{ flex: '1 1 340px' }}
          >
            <div style={{ fontSize: '0.6rem', letterSpacing: '0.3em', textTransform: 'uppercase', color: '#FF3B5C', marginBottom: '1rem' }}>Impact Report</div>
            <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 900, letterSpacing: '-0.03em', marginBottom: '1.5rem', lineHeight: 1.05 }}>
              A DATA-DRIVEN<br />
              <span style={{ color: '#FF3B5C' }}>REVOLUTION</span>
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.45)', lineHeight: 1.75, marginBottom: '2.5rem', fontSize: '1rem' }}>
              Apogee Solutions isn't just a map. It's a decision-support engine that transforms complex geographical and health data into actionable intelligence for policy makers and health officials.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <StatCard value="5.2M" label="Lives Monitored" color="#fff" />
              <StatCard value="42.5%" label="Current Coverage" color="#00B4FF" />
              <StatCard value="38" label="Active Facilities" color="#00FF88" />
              <StatCard value="2 hrs" label="Target Access Limit" color="#FF3B5C" />
            </div>
          </motion.div>

          {/* Right — animated globe rings */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            style={{ flex: '1 1 320px', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >
            <div style={{ position: 'relative', width: 320, height: 320 }}>
              {/* Outer ring */}
              <div style={{ position: 'absolute', inset: 0, borderRadius: '50%', border: '1px solid rgba(0,180,255,0.15)', animation: 'spinSlow 20s linear infinite' }} />
              {/* Mid ring */}
              <div style={{ position: 'absolute', inset: 24, borderRadius: '50%', border: '1px solid rgba(0,180,255,0.25)', animation: 'spinSlow 14s linear infinite reverse' }} />
              {/* Inner */}
              <div style={{ position: 'absolute', inset: 60, borderRadius: '50%', background: 'rgba(0,180,255,0.04)', border: '1px solid rgba(0,180,255,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Globe size={80} color="rgba(0,180,255,0.3)" />
              </div>
              {/* Blurred halo */}
              <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: 160, height: 160, background: 'rgba(0,180,255,0.12)', borderRadius: '50%', filter: 'blur(60px)', pointerEvents: 'none' }} />
              {/* Orbit dot */}
              <div style={{ position: 'absolute', top: 10, right: 30, width: 10, height: 10, borderRadius: '50%', background: '#FF3B5C', boxShadow: '0 0 16px #FF3B5C' }} />
            </div>
          </motion.div>
        </div>
      </section>

      {/* ─── CTA Banner ──────────────────────────────────────────── */}
      <section style={{ padding: '6rem 1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)', background: '#0A0E1A' }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          style={{ maxWidth: 900, margin: '0 auto', textAlign: 'center' }}
        >
          <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 900, letterSpacing: '-0.03em', marginBottom: '1.5rem' }}>
            READY TO EXPLORE
            <br />
            <span style={{ color: '#00B4FF' }}>THE MISSION?</span>
          </h2>
          <p style={{ color: 'rgba(255,255,255,0.4)', marginBottom: '2.5rem', fontSize: '1rem', lineHeight: 1.7 }}>
            Access the live operational dashboard and see real-time surgical coverage intelligence across Liberia.
          </p>
          <motion.button
            onClick={onEnter}
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            style={{
              background: 'linear-gradient(135deg, #00B4FF, #0066FF)',
              color: '#fff',
              padding: '1.2rem 3rem',
              borderRadius: 9999,
              fontWeight: 900,
              fontSize: '0.7rem',
              letterSpacing: '0.18em',
              textTransform: 'uppercase',
              border: 'none',
              cursor: 'pointer',
              boxShadow: '0 0 40px rgba(0,180,255,0.3)',
            }}
          >
            Launch Mission Control
          </motion.button>
        </motion.div>
      </section>

      {/* ─── Footer ──────────────────────────────────────────────── */}
      <footer style={{ padding: '3rem 1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)', background: '#000' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', display: 'flex', flexWrap: 'wrap', gap: '2rem', alignItems: 'center', justifyContent: 'space-between' }}>
          <Logo size={130} />
          <div style={{ display: 'flex', gap: '2rem' }}>
            {['Privacy Policy', 'Terms of Service', 'Contact Mission Control'].map(link => (
              <a
                key={link}
                href="#"
                style={{ fontSize: '0.6rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.35)', textDecoration: 'none', transition: 'color 0.2s' }}
                onMouseEnter={e => e.target.style.color = '#fff'}
                onMouseLeave={e => e.target.style.color = 'rgba(255,255,255,0.35)'}
              >
                {link}
              </a>
            ))}
          </div>
          <div style={{ fontSize: '0.6rem', letterSpacing: '0.15em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.2)' }}>
            © 2026 APOGEE SOLUTIONS. ALL RIGHTS RESERVED.
          </div>
        </div>
      </footer>

      {/* ─── Global Keyframes ─────────────────────────────────────── */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        @keyframes heroZoom   { from { transform: scale(1); } to { transform: scale(1.15); } }
        @keyframes spinSlow   { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes bounce     { 0%,100% { transform: translateY(0); } 50% { transform: translateY(6px); } }
        @keyframes pulse      { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
      `}</style>
    </div>
  );
};

const ObjectiveCard = ({ icon, title, description, accentColor, index }) => (
  <motion.div
    initial={{ opacity: 0, y: 30 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.6, delay: index * 0.15 }}
    whileHover={{ y: -6, borderColor: `${accentColor}40` }}
    style={{
      padding: '2.5rem',
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid rgba(255,255,255,0.08)',
      borderRadius: '1.5rem',
      transition: 'border-color 0.3s, transform 0.3s',
      cursor: 'default',
    }}
  >
    <div style={{ marginBottom: '1.5rem', padding: '0.75rem', display: 'inline-block', borderRadius: '0.75rem', background: `${accentColor}12` }}>
      {icon}
    </div>
    <h3 style={{ fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '1rem', color: '#fff' }}>{title}</h3>
    <p style={{ color: 'rgba(255,255,255,0.4)', lineHeight: 1.7, fontSize: '0.9rem' }}>{description}</p>
  </motion.div>
);

const StatCard = ({ value, label, color }) => (
  <div>
    <div style={{ fontSize: 'clamp(1.75rem, 3vw, 2.5rem)', fontWeight: 900, color, marginBottom: '0.4rem', lineHeight: 1 }}>{value}</div>
    <div style={{ fontSize: '0.6rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.3)' }}>{label}</div>
  </div>
);

export default LandingPage;
