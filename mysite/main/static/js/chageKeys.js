window.onload = function() {
    var buttons = document.querySelectorAll('.button-row');
    var counts = document.querySelectorAll('.Boeken-Count-text');
    
    for (var i = 0; i < buttons.length; i++) {
      var count = parseInt(counts[i].textContent.split(':')[1].trim());
      if (count === 0) {
        buttons[i].querySelector('.buttons').querySelector('a').style.display = 'none';
      }
    }
  };
  