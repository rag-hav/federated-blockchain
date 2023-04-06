import "./App.css";
// import LineChart from "./components/modelGraph.js";
// import Chart from "chart.js/auto";
// import { CategoryScale } from "chart.js";
import React, { useEffect, useState } from "react";
import { Data } from "./utils/Data.js";
import LineChart from "react-linechart";
import "../node_modules/react-linechart/dist/styles.css";
import { Node } from "./node.js";

let node = new Node();
node.connectToContract();

function Timer(props){
  const [timeLeft, setTimeLeft] = useState(0);
  const getSecondsTill = (time)=>{return Date.now()/1000 - time;}
  useEffect(() => {
    const id = setInterval(() => {
      setTimeLeft(getSecondsTill(props.targetTime));
    }, 5000);
    return () => clearInterval(id);
  });
  return timeLeft;

}

function App() {
  const [state, setState] = useState({
    roundEnd: "loading",
    roundNo: "loading",
    state: "loading",
    stateLock: false,
  });

  const [roundDetails, setRoundDetails] = useState({
    arr: [],
  });

  useEffect(() => {
    const id = setInterval(() => {
      node.getState().then((state) => setState(state));
      node.getRoundDetails().then((detail) => setRoundDetails({arr : detail}));
    }, 5000);
    return () => clearInterval(id);
  });

  const getChartData = (arr)=>{
    let res = [
      {
        color: "steelblue",
        points:[],
      },
    ];

    for (let d of arr) {
      if (d.pollCount * d.validationCount > 0)
      res[0].points.push({
        x: d.roundNo,
        y: d.scoreSum / (d.pollCount * d.validationCount * 10000),
      });
    }

    return res;
  };

  
  return (
    <div className="abc">
      <div className="def">
        <dl className="row">
          <dt className="col-sm-3" style={{ marginTop: "10px" }}>
            <b> Current round: </b> <span>{state.roundNo}</span>
          </dt>
          <dt className="col-sm-3" style={{ marginTop: "10px" }}>
            <b> State: </b>
            <span> {state.state == 1 ? "Validating" : "Polling"} </span>
          </dt>
          <dt className="col-sm-3" style={{ marginTop: "10px" }}>
            
            <b> Round end: </b> <span> {
              state.stateLock ? 'infinity' : <Timer targetTime = {parseInt(state.roundEnd)}/>
              } </span>
            

            

          
          </dt>
        </dl>
        <div className="graph">
          {/* <LineChart chartData={chartData}/> */}
          <LineChart
            width={600}
            height={400}
            data={getChartData(roundDetails.arr)}
            xLabel={"Rounds"}
            yLabel={"Average Score"}
            yMax={"100.0"}
            yMin={"0.0"}
            onPointClick={(event, point) => console.log(point)}
            //TODO
            // onPointHover={(point) => }
            // tooltipClass={"svg-line-chart-tooltip"}
          />
        </div>
      </div>
      <div className="def">
        <table id="data">
          <thead>
            <tr>
              <th> Round </th> <th> Poll Count </th> <th> Validation Count </th>
              <th> Average Score </th>
            </tr>
          </thead>

          <tbody>
          {
            roundDetails.arr.map((detail) =>{
              return (
                <tr key = {detail.roundNo}>
                  <th>{detail.roundNo} </th> <th> {detail.pollCount} </th> <th> {detail.validationCount} </th> <th> {detail.scoreSum/(detail.pollCount * detail.validationCount * 10000)} </th>
                </tr>
              );
            })
          }
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
