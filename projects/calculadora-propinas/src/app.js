const inputs = [...document.querySelectorAll('input')];
const bill = document.querySelector('#bill');
const tip = document.querySelector('#tip');
const people = document.querySelector('#people');

function money(value) {
  return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value || 0);
}

function render() {
  const billValue = Math.max(0, Number(bill.value) || 0);
  const tipValue = Math.max(0, Number(tip.value) || 0);
  const peopleValue = Math.max(1, Number(people.value) || 1);
  const tipTotal = billValue * tipValue / 100;
  const total = billValue + tipTotal;
  document.querySelector('#tipTotal').textContent = money(tipTotal);
  document.querySelector('#total').textContent = money(total);
  document.querySelector('#perPerson').textContent = money(total / peopleValue);
}

inputs.forEach(input => input.addEventListener('input', render));
render();
