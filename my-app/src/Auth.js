import React, { Component } from 'react';
import { UserContext } from './UserContext';

const withErrorHandling = WrappedComponent => ({ showError, children }) => {
  return (
    <WrappedComponent>
      {showError && <div className="error-message">Oops! Something went wrong!</div>}
      {children}
    </WrappedComponent>
  );
};

export class Login extends Component {

    static contextType = UserContext;



    constructor(props) {
        super(props);
        this.username = React.createRef();
        this.password = React.createRef();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        console.log('ref to username: ', this.username.current);

        const u = this.username.current.value;
        const p = this.password.current.value;
        console.log('Submitting...', u, p);

        var result ={
          'username' : u,
          'password' : p
        }
        let formBody = [];
      for (let property in result) {
          let encodedKey = encodeURIComponent(property);
          let encodedValue = encodeURIComponent(result[property]);
          formBody.push(encodedKey + "=" + encodedValue);
      }
      formBody = formBody.join("&");

        var request = {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
                'Content-Type':'application/x-www-form-urlencoded'
            },
            body: formBody
        };
        fetch('http://localhost:8765/urlencoded',request).then((response) => response.text())
        .then(text => {
            //store the user's data in local storage
            //to make them available for the next
            //user's visit
            console.log(text)
            if(text == "error: invalid credentials"){
                return
              }
            if(text == "Error: invalid username or password"){
            return
            }
            localStorage.setItem('token', text.token);
            localStorage.setItem('username', u);

            //use the setUserData function available
            //through the UserContext
            this.context.setUserData(text.token, u);

            //use the history prop available through
            //the Route to programmatically navigate
            //to another route
            this.props.history.push('/main');
        });

        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>

                <label htmlFor="username">Username</label>
                <input id="username" type="text" ref={this.username} />

                <label htmlFor="password">Password</label>
                <input id="password" type="password" ref={this.password} />

                <button className="btn btn-primary" type="submit">
                    Login
                </button>
            </form>
        );
    }
}

export class Logout extends Component {

    static contextType = UserContext;

    doLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.clear()

        this.context.setUserData(null, null);

        this.props.history.push('/');
    }

    componentDidMount() {
        //perform an ajax call to logout
        //and then clean up local storage and
        //context state.
        fetch('http://localhost:8765/energy/api/Logout',{
            method: 'POST',
            headers: {

                'Content-Type':'application/x-www-form-urlencoded',
            }
        }).then(() => this.doLogout());
    }

    render() {
        return (<h2>Loggin out...</h2>);
    }
}
