import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Request from 'react-http-request';
import $ from 'jquery';

// Condense all of these classes and methods into one class, look at David's slack for directions

//app
export default class App extends Component{
	render() {
		return (
			<div>
				
				<Search />
			</div>
		)
	}
}



//input

/*
class Input extends Component{
	handleChange() {
		console.log("handling change")
		console.log(this.refs.theGene.value)
		console.log(this.refs.theTerm.value)
		Search.props.render.bind(
			this.refs.theGene.value,
			this.refs.theTerm.value
		);
	}
	render() {
		return (
			<div>
				<form>
					<input type="text" placeholder="Gene" value={this.props.geneSearch} ref="theGene" />
					<input type="text" placeholder="Term" value={this.props.termSearch} ref="theTerm" />
				</form>
				<br></br>
			</div>
		);
	}
}
*/


//search
class Search extends Component{
	constructor() {
		super()
		this.state = {
			clicked: false
		};
		this.handleSubmit = this.handleSubmit.bind(this);
	}
	handleSubmit() {
		this.handleChange();
		this.setState({clicked: true});
	}
	////////////////////////////////////////////////////////////
	handleChange() {
		console.log("handling change")
		console.log(this.refs.theGene.value)
		console.log(this.refs.theTerm.value)
		this.render(
			this.refs.theGene.value,
			this.refs.theTerm.value
		);
	}
	////////////////////////////////////////////////////////////
	render(userGene, userTerm) {
		if (this.state.clicked) {
			return <Listing userGene={this.refs.theGene.value} userTerm={this.refs.theTerm.value}/>
		} else {
			return (
				<div>
					<form>
						<input type="text" placeholder="Gene" value={this.props.geneSearch} ref="theGene" />
						<input type="text" placeholder="Term" value={this.props.termSearch} ref="theTerm" />
					</form>
					<br></br>
						<input type="button" value="Search" onClick={this.handleSubmit} />
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
	loadFromServer(pageToken=0) {
		console.log(pageToken)
		let type = {'content-type': 'application/json'};
		this.serverRequest = $.ajax({ 
			url: "http://localhost:5000/gene/"+this.props.userGene+"/term/"+this.props.userTerm+"/page/"+pageToken, 
			type: "GET", 
			dataType: "json", 
			contentType: "application/json",
			success: (result) => {
				//console.log(this.url) how to do this?
				this.setState({matches: this.state.matches.concat(result.matches)});

				if (result.next_page_token != undefined) {
					// keeps loading previous page in addition to next page, this may be a service issue
					this.loadFromServer(result.next_page_token)
				};
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
		if (this.state.matches.length==0) {
			return <div>loading...</div>
		};
		let allMatches = this.state.matches;
		return (
			<div>
			{allMatches.map((matches) => {
				return(
					<div>
						{matches.biosample.name}
					</div>

				)
			})};
			</div>
		)
	}
}