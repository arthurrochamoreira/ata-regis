// Microsoft Planner Inspired Application
class PlannerApp {
    constructor() {
        this.records = [];
        this.currentEditId = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadMockData();
        this.showBoard();
    }

    bindEvents() {
        // Modal events
        document.getElementById('add-record-btn').addEventListener('click', () => this.openModal());
        document.getElementById('close-modal').addEventListener('click', () => this.closeModal());
        document.getElementById('cancel-btn').addEventListener('click', () => this.closeModal());
        document.getElementById('record-form').addEventListener('submit', (e) => this.saveRecord(e));

        // Dynamic field events
        document.getElementById('add-telefone').addEventListener('click', () => this.addDynamicField('telefones-container', 'tel', 'Telefone'));
        document.getElementById('add-email').addEventListener('click', () => this.addDynamicField('emails-container', 'email', 'E-mail'));
        document.getElementById('add-item').addEventListener('click', () => this.addItemField());

        // Close modal on overlay click
        document.getElementById('record-modal').addEventListener('click', (e) => {
            if (e.target.id === 'record-modal') {
                this.closeModal();
            }
        });

        // Set default date to today
        document.getElementById('data-assinatura').valueAsDate = new Date();
    }

    openModal(record = null) {
        const modal = document.getElementById('record-modal');
        const title = document.getElementById('modal-title');
        
        if (record) {
            title.textContent = 'Editar Ata';
            this.populateForm(record);
            this.currentEditId = record.id;
        } else {
            title.textContent = 'Nova Ata';
            this.clearForm();
            this.currentEditId = null;
            // Set default date
            document.getElementById('data-assinatura').valueAsDate = new Date();
        }
        
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        const modal = document.getElementById('record-modal');
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
        this.clearForm();
        this.currentEditId = null;
    }

    clearForm() {
        document.getElementById('record-form').reset();
        document.getElementById('telefones-container').innerHTML = '';
        document.getElementById('emails-container').innerHTML = '';
        document.getElementById('items-container').innerHTML = '';
    }

    populateForm(record) {
        document.getElementById('numero-ata').value = record.numeroAta || '';
        document.getElementById('documento-sei').value = record.documentoSei || '';
        document.getElementById('objeto').value = record.objeto || '';
        document.getElementById('data-assinatura').value = record.dataAssinatura || '';
        document.getElementById('data-vigencia').value = record.dataVigencia || '';
        document.getElementById('fornecedor').value = record.fornecedor || '';

        // Populate dynamic fields
        const telefonesContainer = document.getElementById('telefones-container');
        telefonesContainer.innerHTML = '';
        (record.telefonesFornecedor || []).forEach(telefone => {
            this.addDynamicField('telefones-container', 'tel', 'Telefone', telefone);
        });

        const emailsContainer = document.getElementById('emails-container');
        emailsContainer.innerHTML = '';
        (record.emailsFornecedor || []).forEach(email => {
            this.addDynamicField('emails-container', 'email', 'E-mail', email);
        });

        // Populate items
        const itemsContainer = document.getElementById('items-container');
        itemsContainer.innerHTML = '';
        (record.items || []).forEach(item => {
            this.addItemField(item);
        });
    }

    addDynamicField(containerId, type, placeholder, value = '') {
        const container = document.getElementById(containerId);
        const div = document.createElement('div');
        div.className = 'dynamic-item';
        
        div.innerHTML = `
            <input type="${type}" placeholder="${placeholder}" value="${value}" required>
            <button type="button" class="remove-item" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(div);
    }

    addItemField(item = {}) {
        const container = document.getElementById('items-container');
        const div = document.createElement('div');
        div.className = 'item-card';
        
        div.innerHTML = `
            <div class="item-header">
                <h4>Item ${container.children.length + 1}</h4>
                <button type="button" class="item-remove" onclick="this.closest('.item-card').remove()">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="form-group">
                <label>Descrição</label>
                <input type="text" class="item-descricao" placeholder="Descrição do item" value="${item.descricao || ''}" required>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Quantidade</label>
                    <input type="number" class="item-quantidade" placeholder="0" value="${item.quantidade || ''}" min="1" required>
                </div>
                <div class="form-group">
                    <label>Valor Unitário (R$)</label>
                    <input type="number" class="item-valor" placeholder="0.00" value="${item.valor || ''}" step="0.01" min="0" required>
                </div>
            </div>
        `;
        
        container.appendChild(div);
    }

    saveRecord(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const record = {
            id: this.currentEditId || this.generateId(),
            numeroAta: document.getElementById('numero-ata').value,
            documentoSei: document.getElementById('documento-sei').value,
            objeto: document.getElementById('objeto').value,
            dataAssinatura: document.getElementById('data-assinatura').value,
            dataVigencia: document.getElementById('data-vigencia').value,
            fornecedor: document.getElementById('fornecedor').value,
            telefonesFornecedor: this.getDynamicFieldValues('telefones-container'),
            emailsFornecedor: this.getDynamicFieldValues('emails-container'),
            items: this.getItemValues(),
            createdAt: this.currentEditId ? this.records.find(r => r.id === this.currentEditId)?.createdAt : new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        if (this.currentEditId) {
            const index = this.records.findIndex(r => r.id === this.currentEditId);
            this.records[index] = record;
            this.showToast('Ata atualizada com sucesso!', 'success');
        } else {
            this.records.push(record);
            this.showToast('Ata criada com sucesso!', 'success');
        }

        this.saveToLocalStorage();
        this.renderRecords();
        this.closeModal();
    }

    getDynamicFieldValues(containerId) {
        const container = document.getElementById(containerId);
        const inputs = container.querySelectorAll('input');
        return Array.from(inputs).map(input => input.value).filter(value => value.trim() !== '');
    }

    getItemValues() {
        const itemCards = document.querySelectorAll('.item-card');
        return Array.from(itemCards).map(card => ({
            descricao: card.querySelector('.item-descricao').value,
            quantidade: parseInt(card.querySelector('.item-quantidade').value) || 0,
            valor: parseFloat(card.querySelector('.item-valor').value) || 0
        }));
    }

    deleteRecord(id) {
        if (confirm('Tem certeza que deseja excluir esta ata? Esta ação não pode ser desfeita.')) {
            this.records = this.records.filter(record => record.id !== id);
            this.saveToLocalStorage();
            this.renderRecords();
            this.showToast('Ata excluída com sucesso!', 'success');
        }
    }

    loadMockData() {
        const savedRecords = localStorage.getItem('plannerRecords');
        if (savedRecords) {
            this.records = JSON.parse(savedRecords);
        } else {
            // Create mock data
            const today = new Date();
            const futureDate = new Date();
            futureDate.setFullYear(today.getFullYear() + 1);
            
            const nearExpiry = new Date();
            nearExpiry.setDate(today.getDate() + 45);
            
            const expired = new Date();
            expired.setDate(today.getDate() - 30);

            this.records = [
                {
                    id: this.generateId(),
                    numeroAta: '0010/2025',
                    documentoSei: '12345.67890/2025-11',
                    objeto: 'Aquisição de Monitores de Vídeo',
                    dataAssinatura: today.toISOString().split('T')[0],
                    dataVigencia: futureDate.toISOString().split('T')[0],
                    fornecedor: 'Tech Solutions LTDA',
                    telefonesFornecedor: ['(61) 99999-8888', '(61) 3333-4444'],
                    emailsFornecedor: ['contato@techsolutions.com'],
                    items: [
                        { descricao: 'Monitor 24" Full HD', quantidade: 50, valor: 899.90 },
                        { descricao: 'Cabo HDMI 2m', quantidade: 50, valor: 25.00 }
                    ],
                    createdAt: today.toISOString(),
                    updatedAt: today.toISOString()
                },
                {
                    id: this.generateId(),
                    numeroAta: '0008/2024',
                    documentoSei: '98765.43210/2024-09',
                    objeto: 'Fornecimento de Material de Escritório',
                    dataAssinatura: new Date(today.getTime() - 300 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    dataVigencia: nearExpiry.toISOString().split('T')[0],
                    fornecedor: 'Papelaria Central EIRELI',
                    telefonesFornecedor: ['(61) 2222-3333'],
                    emailsFornecedor: ['vendas@papelariacentral.com.br'],
                    items: [
                        { descricao: 'Papel A4 75g (resma)', quantidade: 100, valor: 22.50 },
                        { descricao: 'Caneta esferográfica azul', quantidade: 200, valor: 1.20 }
                    ],
                    createdAt: new Date(today.getTime() - 300 * 24 * 60 * 60 * 1000).toISOString(),
                    updatedAt: new Date(today.getTime() - 300 * 24 * 60 * 60 * 1000).toISOString()
                },
                {
                    id: this.generateId(),
                    numeroAta: '0005/2024',
                    documentoSei: '11111.22222/2024-06',
                    objeto: 'Serviços de Limpeza e Conservação',
                    dataAssinatura: new Date(today.getTime() - 400 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    dataVigencia: expired.toISOString().split('T')[0],
                    fornecedor: 'Limpeza Total Serviços LTDA',
                    telefonesFornecedor: ['(61) 4444-5555'],
                    emailsFornecedor: ['contrato@limpezatotal.com.br'],
                    items: [
                        { descricao: 'Serviço de limpeza mensal', quantidade: 12, valor: 2500.00 }
                    ],
                    createdAt: new Date(today.getTime() - 400 * 24 * 60 * 60 * 1000).toISOString(),
                    updatedAt: new Date(today.getTime() - 400 * 24 * 60 * 60 * 1000).toISOString()
                }
            ];
            this.saveToLocalStorage();
        }
    }

    saveToLocalStorage() {
        localStorage.setItem('plannerRecords', JSON.stringify(this.records));
    }

    showBoard() {
        setTimeout(() => {
            document.getElementById('loading-state').classList.add('hidden');
            document.getElementById('kanban-board').classList.remove('hidden');
            this.renderRecords();
        }, 1000);
    }

    renderRecords() {
        const vigentesContainer = document.getElementById('list-vigentes');
        const proximasContainer = document.getElementById('list-proximas');
        const vencidasContainer = document.getElementById('list-vencidas');

        // Clear containers
        vigentesContainer.innerHTML = '';
        proximasContainer.innerHTML = '';
        vencidasContainer.innerHTML = '';

        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const ninetyDaysFromNow = new Date();
        ninetyDaysFromNow.setDate(today.getDate() + 90);

        let vigentesCount = 0;
        let proximasCount = 0;
        let vencidasCount = 0;

        this.records.forEach(record => {
            const [year, month, day] = record.dataVigencia.split('-').map(Number);
            const vigenciaDate = new Date(year, month - 1, day);
            vigenciaDate.setHours(0, 0, 0, 0);

            let container, status, statusClass;
            
            if (vigenciaDate < today) {
                container = vencidasContainer;
                status = 'Vencida';
                statusClass = 'status-vencida';
                vencidasCount++;
            } else if (vigenciaDate <= ninetyDaysFromNow) {
                container = proximasContainer;
                status = 'Vence em breve';
                statusClass = 'status-vencimento';
                proximasCount++;
            } else {
                container = vigentesContainer;
                status = 'Vigente';
                statusClass = 'status-vigente';
                vigentesCount++;
            }

            const card = this.createRecordCard(record, status, statusClass);
            container.appendChild(card);
        });

        // Update counts
        document.getElementById('count-vigentes').textContent = vigentesCount;
        document.getElementById('count-proximas').textContent = proximasCount;
        document.getElementById('count-vencidas').textContent = vencidasCount;

        // Show expiration notifications
        this.checkExpirationNotifications();
    }

    createRecordCard(record, status, statusClass) {
        const card = document.createElement('div');
        card.className = 'card';

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const [vYear, vMonth, vDay] = record.dataVigencia.split('-').map(Number);
        const vigenciaDate = new Date(vYear, vMonth - 1, vDay);

        const [aYear, aMonth, aDay] = record.dataAssinatura.split('-').map(Number);
        const assinaturaDate = new Date(aYear, aMonth - 1, aDay);

        const isExpired = vigenciaDate < today;
        const totalDuration = Math.max(1, (vigenciaDate - assinaturaDate) / (1000 * 60 * 60 * 24));
        const elapsedDuration = Math.max(0, (today - assinaturaDate) / (1000 * 60 * 60 * 24));
        const progress = isExpired ? 100 : Math.min(100, (elapsedDuration / totalDuration) * 100);

        const formattedDate = vigenciaDate.toLocaleDateString('pt-BR');

        card.innerHTML = `
            <div class="card-header">
                <div>
                    <h3 class="card-title">${record.objeto}</h3>
                    <div class="card-meta">
                        <strong>Ata:</strong> ${record.numeroAta} | <strong>SEI:</strong> ${record.documentoSei}
                    </div>
                </div>
                <span class="card-status ${statusClass}">${status}</span>
            </div>
            
            <div class="card-progress">
                <div class="progress-header">
                    <span>Progresso</span>
                    <span>Venc.: ${formattedDate}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progress}%"></div>
                </div>
            </div>
            
            <div class="card-supplier">
                <strong>Fornecedor:</strong> ${record.fornecedor}
            </div>
            
            <div class="card-actions">
                <button class="card-action edit" onclick="app.openModal(app.records.find(r => r.id === '${record.id}'))" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="card-action delete" onclick="app.deleteRecord('${record.id}')" title="Excluir">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return card;
    }

    checkExpirationNotifications() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const ninetyDaysFromNow = new Date();
        ninetyDaysFromNow.setDate(today.getDate() + 90);

        this.records.forEach(record => {
            const [year, month, day] = record.dataVigencia.split('-').map(Number);
            const vigenciaDate = new Date(year, month - 1, day);
            vigenciaDate.setHours(0, 0, 0, 0);

            if (vigenciaDate <= ninetyDaysFromNow && vigenciaDate >= today) {
                const diffTime = Math.abs(vigenciaDate - today);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                const message = `A ata <strong>${record.numeroAta}</strong> vence em ${diffDays} dias.`;
                this.showToast(message, 'warning', 8000);
            }
        });
    }

    showToast(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle',
            info: 'fas fa-info-circle'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <i class="toast-icon ${icons[type]}"></i>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;

        container.appendChild(toast);

        // Auto remove after duration
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, duration);
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
}

// Initialize the application
const app = new PlannerApp();

