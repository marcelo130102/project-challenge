// Variable to control downloading documents
const downloadingDocuments = new Set();

// Verify authentication when loading
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/me');
        if (!response.ok) {
            window.location.href = '/';
            return;
        }
        const user = await response.json();
        document.getElementById('user-info').textContent = `👤 ${user.username} (${user.email})`;
        
        // Load users for the selector
        await loadUsers();
        
        // Load documents
        await loadDocuments();
    } catch (error) {
        window.location.href = '/';
    }
});

// Logout button
document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/';
});

// Load users for the selector
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        if (!response.ok) return;
        
        const users = await response.json();
        const select = document.getElementById('recipient');
        
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = `${user.username} (${user.email})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Upload form button
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('file');
    const recipientId = document.getElementById('recipient').value;
    const viewLimit = document.getElementById('viewLimit').value;
    const expiresInDays = document.getElementById('expiresInDays').value;
    
    formData.append('file', fileInput.files[0]);
    formData.append('recipient_id', recipientId);
    if (viewLimit) formData.append('view_limit', viewLimit);
    if (expiresInDays) formData.append('expires_in_days', expiresInDays);
    
    const uploadMsg = document.getElementById('upload-message');
    const uploadError = document.getElementById('upload-error');
    uploadMsg.style.display = 'none';
    uploadError.style.display = 'none';
    
    try {
        const response = await fetch('/api/documents/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            uploadMsg.textContent = `✓ ${result.message}`;
            uploadMsg.style.display = 'block';
            
            // Reset form
            e.target.reset();
            
            // Reload documents
            await loadDocuments();
        } else {
            const error = await response.json();
            uploadError.textContent = error.detail || 'Error uploading document';
            uploadError.style.display = 'block';
        }
    } catch (error) {
        uploadError.textContent = 'Connection error';
        uploadError.style.display = 'block';
    }
});

// Load documents
async function loadDocuments() {
    try {
        const response = await fetch('/api/documents');
        if (!response.ok) return;
        
        const data = await response.json();
        
        displayDocuments(data.sent, 'sentDocuments', 'sent');
        displayDocuments(data.received, 'receivedDocuments', 'received');
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function displayDocuments(documents, containerId, type) {
    const container = document.getElementById(containerId);
    
    if (documents.length === 0) {
        container.innerHTML = '<p class="no-documents">No documents</p>';
        return;
    }
    
    container.innerHTML = documents.map(doc => {
        const isExpired = doc.is_expired || doc.is_limit_reached;
        const expiresAt = doc.expires_at ? new Date(doc.expires_at).toLocaleString('en-US') : 'No expiration';
        
        let statusBadge = '';
        if (doc.is_expired) {
            statusBadge = '<span class="badge badge-danger">Expired</span>';
        } else if (doc.is_limit_reached) {
            statusBadge = '<span class="badge badge-danger">Limit reached</span>';
        } else if (doc.view_limit && doc.view_count >= doc.view_limit * 0.8) {
            statusBadge = '<span class="badge badge-warning">Near limit</span>';
        }
        
        const downloadButton = !isExpired ? 
            `<button class="btn btn-primary btn-small download-btn" data-doc-id="${doc.id}" data-filename="${doc.filename}">
                ${type === 'received' ? '📥 View/Download' : '👁️ View'}
            </button>` : '';
        
        return `
            <div class="document-card">
                <div class="document-header">
                    <div class="document-filename">📄 ${doc.filename}</div>
                    ${statusBadge}
                </div>
                <div class="document-info">
                    <div><strong>${type === 'sent' ? 'To:' : 'From:'}</strong> ${type === 'sent' ? doc.recipient_username : doc.sender_username}</div>
                    <div><strong>Views:</strong> ${doc.view_count}${doc.view_limit ? ` / ${doc.view_limit}` : ''}</div>
                    <div><strong>Expires:</strong> ${expiresAt}</div>
                    <div><strong>Created:</strong> ${new Date(doc.created_at).toLocaleString('en-US')}</div>
                </div>
                ${downloadButton}
            </div>
        `;
    }).join('');
    
    // Add event listeners for the download buttons
    container.querySelectorAll('.download-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const docId = button.getAttribute('data-doc-id');
            const filename = button.getAttribute('data-filename');
            
            // Disable the button temporarily to avoid double click
            button.disabled = true;
            button.textContent = '⏳ Downloading...';
            
            try {
                await downloadDocument(docId, filename);
            } finally {
                // Re-enable the button after a brief delay
                setTimeout(() => {
                    button.disabled = false;
                    button.textContent = button.textContent.includes('View/Download') ? '📥 View/Download' : '👁️ View';
                }, 2000);
            }
        });
    });
}

async function downloadDocument(documentId, filename) {
    // Verify if the document is already being downloaded
    if (downloadingDocuments.has(documentId)) {
        console.log('Download already in progress for document:', documentId);
        return;
    }
    
    // Mark as downloading
    downloadingDocuments.add(documentId);
    
    try {
        const response = await fetch(`/api/documents/${documentId}/download`);
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.detail || 'Error downloading document');
            // Only reload if the document was deleted (410 Gone)
            if (response.status === 410) {
                await loadDocuments();
            }
            return;
        }
        
        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Reload documents after a delay to update counter
        setTimeout(async () => {
            await loadDocuments();
        }, 1000);
        
    } catch (error) {
        console.error('Error downloading document:', error);
        alert('Error downloading document');
    } finally {
        // Remove from the list of downloading documents
        downloadingDocuments.delete(documentId);
    }
}

// Reload documents every 30 seconds
setInterval(loadDocuments, 30000);

