let authToken = localStorage.getItem('auth_token');
let currentUser = JSON.parse(localStorage.getItem('current_user') || '{}');

if (!authToken || !currentUser.is_admin) {
  window.location.href = '/login.html';
}

const navItems = document.querySelectorAll('.nav-item');
const viewSections = document.querySelectorAll('.view-section');

navItems.forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    const view = item.dataset.view;
    showView(view);
  });
});

function showView(viewName) {
  navItems.forEach(item => item.classList.remove('active'));
  viewSections.forEach(section => section.classList.remove('active'));
  
  document.querySelector(`[data-view="${viewName}"]`).classList.add('active');
  document.getElementById(viewName).classList.add('active');
  
  if (viewName === 'overview') loadDashboard();
  if (viewName === 'knowledge') loadKnowledgeBase();
  if (viewName === 'conversations') loadConversations();
}

async function loadDashboard() {
  const response = await fetch('/api/admin/dashboard', {
    headers: { 'Authorization': `Bearer ${authToken}` }
  });
  const stats = await response.json();
  
  document.getElementById('total-conversations').textContent = stats.total_conversations;
  document.getElementById('total-messages').textContent = stats.total_messages;
  document.getElementById('active-users').textContent = stats.active_users;
  document.getElementById('llm-calls').textContent = stats.llm_calls_today;
}

async function loadKnowledgeBase() {
  const response = await fetch('/api/admin/knowledge-base', {
    headers: { 'Authorization': `Bearer ${authToken}` }
  });
  const items = await response.json();
  
  const kbList = document.getElementById('kb-list');
  kbList.innerHTML = items.map(item => `
    <div class="kb-item">
      <div class="kb-item-header">
        <span class="kb-item-title">${item.key}</span>
        <span style="color: var(--color-text-secondary); font-size: 0.9rem;">${item.category}</span>
      </div>
      <div class="kb-item-content">${item.value}</div>
    </div>
  `).join('');
}

async function loadConversations() {
  const response = await fetch('/api/conversations', {
    headers: { 'Authorization': `Bearer ${authToken}` }
  });
  const conversations = await response.json();
  
  const convList = document.getElementById('conversations-list');
  convList.innerHTML = conversations.slice(0, 10).map(conv => `
    <div class="conversation-item">
      <div style="font-weight: 600; color: var(--color-primary);">${conv.title}</div>
      <div style="font-size: 0.9rem; color: var(--color-text-secondary); margin-top: 4px;">
        ${conv.message_count} messages • ${new Date(conv.updated_at).toLocaleDateString()}
      </div>
    </div>
  `).join('');
}

document.getElementById('logout-btn').addEventListener('click', () => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('current_user');
  window.location.href = '/login.html';
});

// Load dashboard on startup
loadDashboard();
