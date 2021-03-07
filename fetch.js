const axios = require('axios');

axios.get('https://api.trello.com/1/boards/9khsMGic/lists', {
    params: {
        key: 'e1b23f1d39ff82efd37ac98ef2d87ef9',
        token: '512b9358dbf0fe86d032c36ef842133e202c31042a8e69719dd589911fd191a2'
    }
})
.then(({ data }) => {
    data.map(({ id, name }) => {
        console.log(id, name);
    });
});
