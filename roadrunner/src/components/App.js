import React, { Component } from 'react';

class App extends Component {
    authenticateUser = () => {
        window.Trello.authorize({
            type: 'popup',
            name: 'Roadrunner',
            scope: { read: 'true' },
            expiration: 'never',
            success: this.authSuccess,
            error: this.authFailure
          });
    }

    // https://trello.com/1/authorize?response_type=token&key=e1b23f1d39ff82efd37ac98ef2d87ef9&return_url=http://localhost:3000/&callback_method=postMessage&scope=read&expiration=never&name=Roadrunner

    authSuccess = () => {
        console.log(window.Trello.token());
    }
      
    authFailure = () => {
        console.log('Failed authentication');
    }

    render() {
        return (
            <div>
                <div>App</div>
                <button onClick={this.authenticateUser}>Authenticate User</button>
            </div>
        );
    }
}

export default App;