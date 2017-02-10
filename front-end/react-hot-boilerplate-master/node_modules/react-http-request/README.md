# React-http-request

[![npm](https://img.shields.io/npm/v/react-http-request.svg)](https://www.npmjs.com/package/react-http-request)
[![npm](https://img.shields.io/npm/l/react-http-request.svg)](https://github.com/mbasso/react-http-request/blob/master/LICENSE.md)

> React component exposes network request functionality

Useful component to perform a network request and parse the response using [superagent](https://github.com/visionmedia/superagent) module.

## Installation

Using [npm](https://www.npmjs.com/package/react-http-request):

```bash
npm install --save react-http-request
```

Supposing a CommonJS environment, you can simply use the component in this way:

```javascript
import React, { Component } from 'react';
import Request from 'react-http-request';

export default class App extends Component {
  render() {
    return (
      <Request
        url='https://api.github.com/users/mbasso'
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

```

## Documentation

This component use its props to perform a network request based on [superagent](https://github.com/visionmedia/superagent). Here you can find all details about usage.

### Callback

The prop ```children``` of this component would be a function that takes an object as parameter. This object is composed by 3 properties:

|Property   |Description   |
|---|---|
|error   |Contains superagent request error, see [this](http://visionmedia.github.io/superagent/#error-handling) for more information   |
|result   |Contains superagent request response, see [this](http://visionmedia.github.io/superagent/#response-properties) for more information   |
|loading   |True or false, indicates if request is loading or is finished    |

This function will be triggered the first time immediately and second time when request is complete. You can see an example to clarify this concept in Installation section.

### Props

Here is the list of the props used by the component, as we said before, it is based on [superagent](https://github.com/visionmedia/superagent), so, you will find the complete documentation in its site, you will find a link for most props.

|Property   |Type   |Description   |
|---|---|---|
|url   |String    |Request url    |
|method   |String    |Request method: get, head, post, put, delete     |
|children   |function({ error, result, loading }): return node    |Function explained above in "callback" section    |
|type   |String    |Header Content-Type. [docs](http://visionmedia.github.io/superagent/#setting-the-content-type)    |
|accept   |String    |Header Accept. [docs](http://visionmedia.github.io/superagent/#setting-accept)    |
|timeout   |Number    |A timeout after which an error will be triggered. [docs](http://visionmedia.github.io/superagent/#request-timeouts)    |
|verbose   |Boolean    |If true, error messages will automatically be logged to the console    |
|query   |Object or String    |Query parameter. [docs](http://visionmedia.github.io/superagent/#query-strings)    |
|send   |Object or String    |Post parameter. [docs](http://visionmedia.github.io/superagent/#post-/-put-requests)    |
|headers   |Object    |Request header. [docs](http://visionmedia.github.io/superagent/#setting-header-fields)    |
|auth   |{ user: '', pass: '' }    |Basic authentication. [docs](http://visionmedia.github.io/superagent/#basic-authentication)    |
|withCredentials   |Boolean    |Enables the ability to send cookies from the origin, however only when "Access-Control-Allow-Origin" is not a wildcard ("*"), and "Access-Control-Allow-Credentials" is "true". [docs](http://visionmedia.github.io/superagent/#cors)    |
|buffer   |Boolean    |To force buffering of response bodies as result.text. [docs](http://visionmedia.github.io/superagent/#buffering-responses)    |
|attach   |Array of { name: '', path: '', filename: '' }    |Attach files. [docs](http://visionmedia.github.io/superagent/#multipart-requests)    |
|fields   |Array of { name: '', value: '' }    |Much like form fields in HTML, you can set field values. [docs](http://visionmedia.github.io/superagent/#multipart-requests)    |
|onRequest   |function(request): return request   |Function that will be called before sending the request. It accept as parameter the request itself and must return the request. This means that you can manually modify the request that will be sent.     |


## Author
**Matteo Basso**
- [github/mbasso](https://github.com/mbasso)
- [@Teo_Basso](https://twitter.com/Teo_Basso)

## Copyright and License
Copyright (c) 2016, Matteo Basso.

React-http-request source code is licensed under the [MIT License](https://github.com/mbasso/react-http-request/blob/master/LICENSE.md).
