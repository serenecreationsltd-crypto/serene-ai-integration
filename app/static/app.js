body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: linear-gradient(135deg, #f7f3ee, #f0ebe7 50%, #e8e1db);
  color: #1d1b1a;
}

.shell {
  max-width: 1080px;
  margin: 0 auto;
  padding: 32px 20px 64px;
}

.topbar {
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: #7d645e;
  margin-bottom: 6px;
}

h1 {
  margin: 0;
  font-size: clamp(2rem, 5vw, 3.5rem);
  color: #1d1b1a;
}

.chat-panel {
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(93, 74, 69, 0.1);
  border-radius: 24px;
  backdrop-filter: blur(8px);
  box-shadow: 0 20px 60px rgba(35, 23, 19, 0.08);
  padding: 18px;
}

.messages {
  min-height: 420px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.bot-message,
.user-message {
  max-width: 75%;
  border-radius: 18px;
  padding: 14px 16px;
  line-height: 1.5;
}

.bot-message {
  background: #f0e9e5;
  color: #2a2321;
  align-self: flex-start;
}

.user-message {
  background: #2f2a28;
  color: #f7f3ee;
  align-self: flex-end;
}

.composer {
  display: flex;
  gap: 12px;
}

.composer input {
  flex: 1;
  border: 1px solid rgba(84, 64, 58, 0.15);
  background: rgba(255, 255, 255, 0.7);
  border-radius: 14px;
  padding: 14px 16px;
  font-size: 1rem;
}

.composer button {
  border: none;
  background: #231f1d;
  color: #f5f1ee;
  border-radius: 14px;
  padding: 14px 20px;
  font-size: 1rem;
  cursor: pointer;
}

@media (max-width: 600px) {
  .composer {
    flex-direction: column;
  }

  .bot-message,
  .user-message {
    max-width: 100%;
  }
}
