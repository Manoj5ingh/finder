import React, { Component } from "react";
import { render } from "react-dom";
import AllInOne from './AllInOne';
import axios from 'axios';

export default class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
        <div>
            <AllInOne/>
        </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
