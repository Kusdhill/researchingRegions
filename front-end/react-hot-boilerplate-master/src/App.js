import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Request from 'react-http-request';
import $ from 'jquery';


/*
// sends request to gene search service
export default class App extends Component {
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
		)
	}
}
*/






//app
export default class App extends Component{
	render() {
		return (
			<HelloMessage />
		)
	}
}



// Testing
/////////////////////////////////////////////////////////////////////////////////////////////////////////////


//listing
class HelloMessage extends Component{
	constructor() {
		super()
		this.state = {
			matches: []
		}
	}
	loadFromServer(pageToken=null) {
		let type = {'content-type': 'application/json'};
		this.serverRequest = $.ajax({ 
			url: "http://localhost:5000/gene/BRCA1/term/SO:0001630/page/0", 
			type: "GET", 
			dataType: "json", 
			contentType: "application/json", 
			success: (result) => {
				this.setState({matches: this.state.matches.concat(result.matches)});

				if (result.nextPageToken != "") {
					this.loadFromServer(result.nextPageToken)
				}
			},
			error: (xhr, status, err) => {
				console.log(err);
			}
		});
	}
	componentDidMount() {
		this.loadFromServer();
	}
	componentWillUnmount() {
		this.serverRequest.abort();
	}
	render() {
		console.log(this.state.matches)
		if (this.state.matches.length==0) {
			return <div>loading...</div>
		}
		let allMatches = this.state.matches;
		return (
			<div>
			{allMatches.map((matches) => {
				return <div>{matches.biosample.name}</div>
			})}
			</div>
		)
	}
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////





/*

// renders searchBox and results
var App = React.createClass({
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



ReactDOM.render(<app />, document.getElementById("content"));
*/