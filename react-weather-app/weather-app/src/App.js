import React, { Component } from 'react';
import './App.css';
import List from './List';
import Titles from './Titles';
import Form from './Form';
import Weather from './Weather';


const API_KEY = "daeda48c1893b6c25a6eabb049259e70"


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
        weatherData: {
        temperature: undefined,
        pressure: undefined,
        city: undefined,
        country: undefined,
        humidity: undefined,
        description: undefined,
        error: undefined
      },
      items: []
    }
  }

  getWeather = async (event) => {
    event.preventDefault();
    const city = event.target.elements.city.value;

    const country = event.target.elements.country.value;

    const api_call = await fetch(`http://api.openweathermap.org/data/2.5/weather?q=${city},${country}&appid=${API_KEY}`);
    const response = await api_call.json();

    var weatherData = {
      temperature: response.main.temp,
      pressure: response.main.pressure,
      city: response.name,
      country: response.sys.country,
      humidity: response.main.humidity,
      description: response.weather[0].description,
      error: ""
    }
    this.setState({
      items: [weatherData, ...this.state.items]
    })


    console.log(response);

  }

  render() {
    return (
      <div>
        <Titles />
        <Form loadWeather={this.getWeather} />
        <Weather
          temperature={this.state.temperature}
          city={this.state.city}
          country={this.state.country}
          humidity={this.state.humidity}
          description={this.state.description}
          error={this.state.error} />

        <List items={this.state.items} />
      </div>
    );
  }
}

module.exports = App;