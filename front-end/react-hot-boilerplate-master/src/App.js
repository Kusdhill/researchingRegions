import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Request from 'react-http-request';

// sends request to gene search service
var request = React.createClass({
	render() {
		return (
			<Request
				url='http://localhost:5000/gene/APP/term/SO:0001630/page/0'
				method='get'
				accept='application/json'
				verbose={true}
			>
				{
					({error, result, loading}) => {
						if (loading) {
							return <div>loading...</div>;
						} else {
							return <div>{ JSON.stringify(result) }</div>;
						}
					}
				}
			</Request>
		);
	}
});

/*

// renders searchBox and results
var app = React.createClass({
	render: function(){
		return(
			<div>
				<searchBox />
				<results />
			</div>
		);
	}
});



// renders resultItems
var results = React.createClass({
	render: function(){
		return(
			<ul>
				<resultItems />
			</ul>
		);
	}
});



// renders search result items
var resultItems = React.createClass({
	render: function(){
		return <li>"search result item"</li>;
	}
});

*/

ReactDOM.render(<app />, document.getElementById("root"));

