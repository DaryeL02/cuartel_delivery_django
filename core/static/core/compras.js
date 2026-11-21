const API_BASE = '/api';
const TOKEN_KEY = 'cuartel-token';

const loginPanel = document.querySelector('#login-panel');
const appPanel = document.querySelector('#app-panel');
const notice = document.querySelector('#notice');
const loginForm = document.querySelector('#login-form');
const purchaseForm = document.querySelector('#purchase-form');
const supplierSelect = document.querySelector('#supplier');
const cashAmount = document.querySelector('#cash-amount');
const transferAmount = document.querySelector('#transfer-amount');
const itemsBody = document.querySelector('#purchase-items');
const purchasesList = document.querySelector('#purchases-list');
const emptyPurchases = document.querySelector('#empty-purchases');
const logoutButton = document.querySelector('#logout-button');

let token = localStorage.getItem(TOKEN_KEY);
let suppliers = [];
let supplies = [];
let supplierSupplyIds = [];
let supplierRelations = [];

function showNotice(message, isError = false) {
    notice.textContent = message;
    notice.classList.toggle('error', isError);
    notice.classList.remove('hidden');
}

function hideNotice() {
    notice.classList.add('hidden');
}

function showLogin() {
    loginPanel.classList.remove('hidden');
    appPanel.classList.add('hidden');
    logoutButton.classList.add('hidden');
}

function showApplication() {
    loginPanel.classList.add('hidden');
    appPanel.classList.remove('hidden');
    logoutButton.classList.remove('hidden');
}

function responseMessage(data, fallback) {
    if (typeof data === 'string') return data;
    if (data && typeof data === 'object') {
        return Object.values(data).flat().join(' ') || fallback;
    }
    return fallback;
}

async function apiRequest(path, options = {}) {
    const headers = { ...(options.headers || {}) };
    if (token) headers.Authorization = `Token ${token}`;
    if (options.body) headers['Content-Type'] = 'application/json';

    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    const data = response.status === 204 ? null : await response.json();

    if (!response.ok) {
        if (response.status === 401) {
            logout();
        }
        throw new Error(responseMessage(data, 'No se pudo completar la solicitud.'));
    }
    return data;
}

function records(data) {
    return Array.isArray(data) ? data : (data.results || []);
}

function addOption(select, value, label) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = label;
    select.append(option);
}

function fillSelect(select, items, getId, getName, placeholder) {
    select.replaceChildren();
    addOption(select, '', placeholder);
    items.forEach((item) => addOption(select, getId(item), getName(item)));
}

function updateSupplyOptions(row) {
    const currentValue = row.querySelector('.supply-select').value;
    const available = supplies.filter((supply) => supplierSupplyIds.includes(supply.id_insumos));
    const select = row.querySelector('.supply-select');
    fillSelect(select, available, (item) => item.id_insumos, (item) => item.nombre, 'Selecciona un insumo');
    if (available.some((item) => String(item.id_insumos) === currentValue)) {
        select.value = currentValue;
    }
}

function createItemRow() {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td><select class="supply-select" required aria-label="Insumo"></select></td>
        <td><input class="quantity-input" type="number" min="1" step="1" value="1" required aria-label="Cantidad"></td>
        <td><input class="subtotal-input" type="number" min="0" step="0.01" value="0.00" required aria-label="Subtotal"></td>
        <td><button class="button button-secondary remove-item" type="button" aria-label="Quitar insumo">Quitar</button></td>
    `;
    updateSupplyOptions(row);
    row.querySelector('.quantity-input').addEventListener('input', updateTotal);
    row.querySelector('.subtotal-input').addEventListener('input', updateTotal);
    row.querySelector('.remove-item').addEventListener('click', () => {
        row.remove();
        updateTotal();
    });
    itemsBody.append(row);
}

function updateTotal() {
    const totalCents = [...itemsBody.querySelectorAll('.subtotal-input')]
        .reduce((sum, input) => sum + Math.round((Number(input.value) || 0) * 100), 0);
    document.querySelector('#purchase-total').textContent = (totalCents / 100).toFixed(2);
}

async function loadPurchases() {
    const data = records(await apiRequest('/compras/'));
    purchasesList.replaceChildren();
    emptyPurchases.classList.toggle('hidden', data.length > 0);

    data.forEach((purchase) => {
        const row = document.createElement('tr');
        const date = purchase.fecha_hora_creacion
            ? new Date(purchase.fecha_hora_creacion).toLocaleString('es-AR')
            : '—';
        const details = (purchase.detalles || [])
            .map((detail) => `${detail.insumo_data?.nombre || 'Insumo'} × ${detail.cantidad}`)
            .join(', ');
        const payments = [];
        if (Number(purchase.monto_efectivo) > 0) {
            payments.push(`Efectivo: $${Number(purchase.monto_efectivo).toFixed(2)}`);
        }
        if (Number(purchase.monto_transferencia) > 0) {
            payments.push(`Transferencia: $${Number(purchase.monto_transferencia).toFixed(2)}`);
        }
        [
            `#${purchase.id_compras}`,
            date,
            purchase.proveedor_data?.nombre || 'Sin proveedor',
            payments.join(' / ') || purchase.metodo_data?.nombre || 'Sin pagos',
            details || '—',
            `$${Number(purchase.precio_total).toFixed(2)}`,
        ].forEach((value) => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.append(cell);
        });
        purchasesList.append(row);
    });
}

async function loadApplicationData() {
    showApplication();
    hideNotice();
    try {
        const [supplierData, supplyData, relationData] = await Promise.all([
            apiRequest('/proveedores/'),
            apiRequest('/insumos/'),
            apiRequest('/proveedores-insumos/'),
        ]);
        suppliers = records(supplierData);
        supplies = records(supplyData);
        supplierRelations = records(relationData);

        fillSelect(supplierSelect, suppliers, (item) => item.id_proveedores, (item) => item.nombre, 'Selecciona un proveedor');
        supplierSelect.dispatchEvent(new Event('change'));
        await loadPurchases();
        showNotice('Datos cargados. Ya puedes registrar compras.');
    } catch (error) {
        showNotice(error.message, true);
    }
}

supplierSelect.addEventListener('change', async () => {
    if (!supplierSelect.value) {
        supplierSupplyIds = [];
    } else {
        supplierSupplyIds = supplierRelations
            .filter((relation) => String(relation.proveedor) === supplierSelect.value)
            .map((relation) => relation.insumo);
    }
    itemsBody.querySelectorAll('tr').forEach(updateSupplyOptions);
});

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    hideNotice();
    const submitButton = loginForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    try {
        const response = await fetch(`${API_BASE}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                usuario: loginForm.elements.usuario.value,
                password: loginForm.elements.password.value,
            }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(responseMessage(data, 'Usuario o contraseña incorrectos.'));
        token = data.token;
        localStorage.setItem(TOKEN_KEY, token);
        await loadApplicationData();
    } catch (error) {
        showNotice(error.message, true);
    } finally {
        submitButton.disabled = false;
    }
});

purchaseForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    hideNotice();
    const button = purchaseForm.querySelector('button[type="submit"]');
    button.disabled = true;
    const detalles = [...itemsBody.querySelectorAll('tr')].map((row) => ({
        insumo: Number(row.querySelector('.supply-select').value),
        cantidad: Number(row.querySelector('.quantity-input').value),
        subtotal: Number(row.querySelector('.subtotal-input').value).toFixed(2),
    }));
    const totalCents = detalles.reduce((sum, detail) => sum + Math.round(Number(detail.subtotal) * 100), 0);
    const cashCents = Math.round((Number(cashAmount.value) || 0) * 100);
    const transferCents = Math.round((Number(transferAmount.value) || 0) * 100);

    if (
        cashAmount.value === '' ||
        transferAmount.value === '' ||
        Number(cashAmount.value) < 0 ||
        Number(transferAmount.value) < 0 ||
        cashCents + transferCents > totalCents
    ) {
        showNotice('Los pagos deben ser válidos y no pueden superar el total de la compra.', true);
        button.disabled = false;
        return;
    }

    try {
        await apiRequest('/compras/', {
            method: 'POST',
            body: JSON.stringify({
                proveedor: Number(supplierSelect.value),
                monto_efectivo: (cashCents / 100).toFixed(2),
                monto_transferencia: (transferCents / 100).toFixed(2),
                detalles,
            }),
        });
        purchaseForm.reset();
        cashAmount.value = '0.00';
        transferAmount.value = '0.00';
        itemsBody.replaceChildren();
        createItemRow();
        updateTotal();
        await loadPurchases();
        showNotice('Compra registrada y stock actualizado correctamente.');
    } catch (error) {
        showNotice(error.message, true);
    } finally {
        button.disabled = false;
    }
});

document.querySelector('#add-item').addEventListener('click', createItemRow);
document.querySelector('#refresh-purchases').addEventListener('click', () => {
    loadPurchases().catch((error) => showNotice(error.message, true));
});

function logout() {
    token = null;
    localStorage.removeItem(TOKEN_KEY);
    showLogin();
}

logoutButton.addEventListener('click', logout);

if (token) {
    loadApplicationData();
} else {
    showLogin();
}
