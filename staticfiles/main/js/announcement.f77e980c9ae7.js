document.addEventListener('DOMContentLoaded', function() {
    // File upload handling for announcement form
    const fileInput = document.getElementById('attachments');
    const fileList = document.getElementById('file-list');
    
    if (fileInput && fileList) {
        fileInput.addEventListener('change', function() {
            fileList.innerHTML = '';
            
            if (this.files.length > 0) {
                const header = document.createElement('p');
                header.textContent = 'Selected files:';
                header.style.fontWeight = '500';
                header.style.marginBottom = '0.5rem';
                fileList.appendChild(header);
                
                for (let i = 0; i < this.files.length; i++) {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-list-item';
                    
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-file-alt';
                    
                    const name = document.createElement('span');
                    name.className = 'file-list-item-name';
                    name.textContent = this.files[i].name;
                    
                    const remove = document.createElement('span');
                    remove.className = 'file-list-item-remove';
                    remove.innerHTML = '&times;';
                    remove.addEventListener('click', function() {
                        // In a real implementation, you would need to handle file removal
                        fileItem.remove();
                    });
                    
                    fileItem.appendChild(icon);
                    fileItem.appendChild(name);
                    fileItem.appendChild(remove);
                    fileList.appendChild(fileItem);
                }
            }
        });
    }
    
    // Drag and drop for file upload
    const fileUploadLabel = document.querySelector('.file-upload-label');
    if (fileUploadLabel) {
        fileUploadLabel.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = red;
            this.style.backgroundColor = 'rgba(26, 90, 150, 0.1)';
        });
        
        fileUploadLabel.addEventListener('dragleave', function() {
            this.style.borderColor = '#ddd';
            this.style.backgroundColor = 'transparent';
        });
        
        fileUploadLabel.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#ddd';
            this.style.backgroundColor = 'transparent';
            
            if (fileInput) {
                fileInput.files = e.dataTransfer.files;
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        });
    }
});