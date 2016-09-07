import React, { Component } from 'react';
import Request from 'react-http-request';

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
		);
	}
}

