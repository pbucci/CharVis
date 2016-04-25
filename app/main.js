import React from 'react';
var Main = require('./main.jsx');
require('../css/style.css');

main();

function main() {
	React.render(<Main />, document.getElementById('app'));
}