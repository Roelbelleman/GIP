const button = document.querySelector('button');
let doneClicked = false;

button.addEventListener('click', function(event) {
  if (!doneClicked) {
    event.preventDefault();
    const form = document.querySelector('form');
    form.submit();
    button.innerHTML = 'klaar';
    doneClicked = true;
    setTimeout(function() {
      window.location.href = '/makebagpack';
    }, 50);
  } else {
    event.preventDefault();
    window.location.href = '/makebagpackDoneV';
  }
});

window.onload = function() {
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0');
  var yyyy = today.getFullYear();

  if (today.getHours() < 12) {
    today = yyyy + '-' + mm + '-' + dd;
  } else {
    var tomorrow = new Date(today.getTime() + (24 * 60 * 60 * 1000));
    var dd = String(tomorrow.getDate()).padStart(2, '0');
    var mm = String(tomorrow.getMonth() + 1).padStart(2, '0');
    var yyyy = tomorrow.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;
  }

  document.getElementById("datafield").value = today;
  hideNonCurrentDays()
};

const dateInput = document.getElementById('datafield');
dateInput.addEventListener('change', function() {
  hideNonCurrentDays()
});

function hideNonCurrentDays() {
  const selectedDate = new Date(dateInput.value);
  const dayOfWeek = selectedDate.getDay(); 
  var days = document.querySelectorAll('.agenda-maandag, .agenda-dinsdag, .agenda-woensdag, .agenda-donderdag, .agenda-vrijdag');

  days.forEach(function(day) {
    day.style.display = 'none';
  });
  
  switch(dayOfWeek) {
    case 1:
      document.querySelector('.agenda-maandag').style.display = 'block';
      break;
    case 2:
      document.querySelector('.agenda-dinsdag').style.display = 'block';
      break;
    case 3:
      document.querySelector('.agenda-woensdag').style.display = 'block';
      break;
    case 4:
      document.querySelector('.agenda-donderdag').style.display = 'block';
      break;
    case 5:
      document.querySelector('.agenda-vrijdag').style.display = 'block';
      break;
    default:
      break;
  }
}