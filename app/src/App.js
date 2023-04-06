import './App.css';
import "./App.css";
// import LineChart from "./components/modelGraph.js";
// import Chart from "chart.js/auto";
// import { CategoryScale } from "chart.js";
import React, { useState } from "react";
import { Data } from "./utils/Data.js";
import LineChart from 'react-linechart';
import '../node_modules/react-linechart/dist/styles.css';

// Chart.register(CategoryScale);

function App() {

    const chartData = [{
        color: "steelblue",
        points: Data,
    }];

    // function handletooltip(point) {
    //   return
    // }

    return ( <
        div className = "abc" >
        <
        div className = "def" >
        <
        dl className = "row" >

        <
        dt className = "col-sm-3"
        style = {
            { marginTop: "10px" } } > < b > Current round: < /b> <span>18</span > < /dt>

        <
        dt className = "col-sm-3"
        style = {
            { marginTop: "10px" } } > < b > State: < /b><span>Polling</span > < /dt>

        <
        dt className = "col-sm-3"
        style = {
            { marginTop: "10px" } } > < b > Round end: < /b><span>30</span > < /dt>

        <
        /dl>

        <
        div className = "graph" > { /* <LineChart chartData={chartData}/> */ } <
        LineChart width = { 600 }
        height = { 400 }
        data = { chartData }
        xLabel = { "Rounds" }
        yLabel = { "Average Score" }
        yMax = { "100.0" }
        yMin = { "0.0" }
        onPointClick = {
            (event, point) => console.log(point) }
        //TODO
        // onPointHover={(point) => }
        // tooltipClass={"svg-line-chart-tooltip"}
        /> <
        /div> <
        /div>

        <
        div className = "def" >
        <
        table id = "data" >
        <
        tbody >

        <
        tr >
        <
        th > Round < /th> <
        th > Poll Count < /th> <
        th > Validation Count < /th> <
        th > Average Score < /th> <
        /tr> <
        tr >
        <
        th > 1 < /th> <
        th > 3 < /th> <
        th > 3 < /th> <
        th > 70.19 < /th> <
        /tr> <
        tr >
        <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 71.22 < /th> <
        /tr> <
        tr >
        <
        th > 3 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 69.90 < /th> <
        /tr> <
        tr >
        <
        th > 4 < /th> <
        th > 3 < /th> <
        th > 3 < /th> <
        th > 72.11 < /th> <
        /tr> <
        tr >
        <
        th > 5 < /th> <
        th > 3 < /th> <
        th > 2 < /th> <
        th > 70.99 < /th> <
        /tr> <
        tr >
        <
        th > 6 < /th> <
        th > 4 < /th> <
        th > 4 < /th> <
        th > 70.09 < /th> <
        /tr> <
        tr >
        <
        th > 7 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 71.22 < /th> <
        /tr> <
        tr >
        <
        th > 8 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 71.99 < /th> <
        /tr> <
        tr >
        <
        th > 9 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 70.99 < /th> <
        /tr> <
        tr >
        <
        th > 10 < /th> <
        th > 2 < /th> <
        th > 1 < /th> <
        th > 69.90 < /th> <
        /tr> <
        tr >
        <
        th > 11 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 72.11 < /th> <
        /tr> <
        tr >
        <
        th > 12 < /th> <
        th > 1 < /th> <
        th > 1 < /th> <
        th > 70.99 < /th> <
        /tr> <
        tr >
        <
        th > 13 < /th> <
        th > 2 < /th> <
        th > 2 < /th> <
        th > 68.02 < /th> <
        /tr> <
        tr >
        <
        th > 14 < /th> <
        th > 6 < /th> <
        th > 5 < /th> <
        th > 70.19 < /th> <
        /tr> <
        tr >
        <
        th > 15 < /th> <
        th > 6 < /th> <
        th > 5 < /th> <
        th > 69.07 < /th> <
        /tr> <
        tr >
        <
        th > 16 < /th> <
        th > 6 < /th> <
        th > 5 < /th> <
        th > 66.99 < /th> <
        /tr> <
        tr >
        <
        th > 17 < /th> <
        th > 6 < /th> <
        th > 5 < /th> <
        th > 69.77 < /th> <
        /tr> <
        tr >
        <
        th > 18 < /th> <
        th > 6 < /th> <
        th > 5 < /th> <
        th > 70.11 < /th> <
        /tr> <
        /tbody> <
        /table> <
        /div>

        <
        /div>
    );
}

export default App;