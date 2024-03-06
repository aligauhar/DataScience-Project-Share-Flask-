  setTimeout(function() {
    var alertSuccessDivs = document.getElementsByClassName('alert-success');
    for (var i = 0; i < alertSuccessDivs.length; i++) {
      alertSuccessDivs[i].style.display = "none";
    }

    var alertDivs = document.getElementsByClassName('alert');
    for (var j = 0; j < alertDivs.length; j++) {
      alertDivs[j].style.display = "none";
    }
}, 5000);