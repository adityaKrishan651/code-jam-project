var events = [];

var settings = {};
var element = document.getElementById('calendar');

const dates_and_events = document.getElementsByClassName('event-and-date');
for(let i = 0; i < dates_and_events.length; i++) {
    let array = dates_and_events[i].innerText.split('$');
    let date = array[0].split('-');
    let title = array[1];
    events.push({'Date': new Date(date[0], date[1]-1, date[2]), 'Title': title + "."});
}

calendar(element, events, settings);
