import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Request from 'react-http-request';
import $ from 'jquery';



//app
export default class App extends Component{
	render() {
		return (
			<div>
				<Input />
				<Search />
			</div>
		)
	}
}


//input
class Input extends Component{
	render() {
		return (
			<form>
				<input type="text" placeholder="Gene" />
				<input type="text" placeholder="Term" />
				<input type="text" placeholder="Page" />
			</form>
		);
	}
}



//search
class Search extends Component{
	constructor() {
		super()
		this.state = {
			clicked: false
		}
	}
	render() {
		if (this.state.clicked) {
			return <Listing {... this.params} />
		} else {
			return (
				<div>
					<div>Please enter a query</div>
					<input type="button" value="Search" onClick={this.setState({clicked: true})} />
				</div>
			)
		}
	}
}



//listing
class Listing extends Component{
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