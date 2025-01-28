const apiUrl = 'http://127.0.0.1:8000/api/';

// Função de login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(apiUrl + 'token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Login bem-sucedido!');
        localStorage.setItem('access_token', data.access);
    } else {
        alert('Erro ao fazer login: ' + data.detail);
    }
}

// Função de registro de fornecedor
async function registerSupplier() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch(apiUrl + 'register-supplier/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Fornecedor registrado com sucesso!');
    } else {
        alert('Erro: ' + data.detail);
    }
}

// Função de registrar produto
async function registerProduct() {
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    const price = document.getElementById('price').value;
    const stock = document.getElementById('stock').value;
    const token = localStorage.getItem('access_token');

    const response = await fetch(apiUrl + 'register-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, description, price, stock })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Produto registrado com sucesso!');
    } else {
        alert('Erro: ' + data.detail);
    }
}

// Função de criar pedido
async function createOrder() {
    const product_id = document.getElementById('product_id').value;
    const quantity = document.getElementById('quantity').value;
    const token = localStorage.getItem('access_token');

    const response = await fetch(apiUrl + 'create-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            items: [{ product_id, quantity }]
        })
    });

    const data = await response.json();

    if (response.ok) {
        alert('Pedido criado com sucesso!');
    } else {
        alert('Erro: ' + data.detail);
    }
}
