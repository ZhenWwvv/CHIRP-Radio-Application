'use strict';

$(document).on('webSocketMessage', (evt, obj) => {
  if (obj.type === 'count') {
    let p = $('p.extra')
    p.find('.count').text(obj.count)
    p.find('.elapsed').text(Math.round(obj.elapsed_seconds))
    let rate = obj.count / obj.elapsed_seconds
    p.find('.rate').text(rate.toFixed(2))
  }
})
