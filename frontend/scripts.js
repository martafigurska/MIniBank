document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('login-view');
    const accountView = document.getElementById('account-view');
    const loginForm = document.getElementById('login-form');
    const transactionForm = document.getElementById('transaction-form');
    const accountInfo = document.getElementById('account-info');
    const transactionHistory = document.getElementById('transaction-history');
    const logoutButton = document.getElementById('logout-button');
    let account_id = -1;

    let loggedIn = false;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        account_id = parseInt(document.getElementById('account_id').value);
        const response = await fetch('http://127.0.0.1:8000/login/' + account_id + '/' + document.getElementById('password').value);
        const login = await response.json();
        if (login.login != 'success') {
            alert('Invalid login data!');
            console.log(login);
            return;
        }
        loggedIn = true;
        loginView.style.display = 'none';
        accountView.style.display = 'block';
        loadAccountData();
    });

    logoutButton.addEventListener('click', () => {
        loggedIn = false;
        accountView.style.display = 'none';
        loginView.style.display = 'block';
        loginForm.reset();
        accountInfo.innerHTML = '';
        transactionHistory.innerHTML = '';
    });

    transactionForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const desAccount = document.getElementById('des_account').value;
        const amount = document.getElementById('amount').value;
        await createTransaction(desAccount, amount);
        loadTransactionHistory();
    });

    async function loadAccountData() {
        const response = await fetch('http://127.0.0.1:8000/account/' + account_id);
        const account = await response.json();
        accountInfo.innerHTML = `
            <p>Account ID: ${account_id}</p>
            <p>Name: ${account.imie} ${account.nazwisko}</p>
            <p>Balance: ${account.saldo}</p>
        `;
        loadTransactionHistory();
    }

    async function loadTransactionHistory() {
        const response = await fetch('http://127.0.0.1:8000/transactions/' + account_id);
        const transactions = await response.json();
        transactionHistory.innerHTML = transactions.map(tx => `
            <p>Transaction ID: ${tx.nr_transakcji} | Amount: ${tx.kwota}</p>
        `).join('');
    }

    async function createTransaction(desAccount, amount) {
        await fetch('http://127.0.0.1:8000/new_transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                src_account: account_id,
                des_account: parseInt(desAccount),
                amount: parseFloat(amount)
            })
        });
    }
});
