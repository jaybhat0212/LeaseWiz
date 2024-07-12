import React, { useState, useEffect } from "react";

const Results = ({
  prediction,
  listPrice,
  originalBeds,
  originalBaths,
  results,
}) => {
  const roundToNearest25 = (num) => {
    return Math.round(num / 25) * 25;
  };

  const roundedPrediction = roundToNearest25(prediction);
  const lowerBound = roundedPrediction - 125;
  const upperBound = roundedPrediction + 125;

  const [beds, setBeds] = useState(originalBeds);
  const [baths, setBaths] = useState(originalBaths);
  const [newPrediction, setNewPrediction] = useState(results.predicted_price);
  const [selectedCity, setSelectedCity] = useState(
    results.city_prediction[0][0]
  );
  const [cityPrediction, setCityPrediction] = useState(
    results.city_prediction[0][1]
  );

  useEffect(() => {
    if (beds > originalBeds) {
      setNewPrediction(results.bed_higher_prediction);
    } else if (beds < originalBeds) {
      setNewPrediction(results.bed_lower_prediction);
    } else if (baths > originalBaths) {
      setNewPrediction(results.bath_higher_prediction);
    } else if (baths < originalBaths) {
      setNewPrediction(results.bath_lower_prediction);
    } else if (baths > originalBaths) {
      setNewPrediction(results.predicted_price);
    } else {
      setNewPrediction(results.predicted_price);
    }
  }, [beds, baths, originalBeds, originalBaths, results]);

  useEffect(() => {
    if (selectedCity == results.city_prediction[0][0]) {
      setCityPrediction(results.city_prediction[0][1]);
    } else if (selectedCity == results.city_prediction[1][0]) {
      setCityPrediction(results.city_prediction[1][1]);
    }
  }, [selectedCity, results]);

  var markerPosition;
  var rangeFillColor;
  var explanation = [];

  if (listPrice < lowerBound) {
    markerPosition = "0%";
    rangeFillColor = "green";
    explanation.push("less than");
    explanation.push("a good");
  } else if (listPrice > upperBound) {
    markerPosition = "100%";
    rangeFillColor = "red";
    explanation.push("more than");
    explanation.push("overpriced");
  } else {
    markerPosition = "50%";
    rangeFillColor = "yellow";
    explanation.push("within");
    explanation.push("an expected");
  }

  const handleBedsChange = (e) => {
    setBeds(Number(e.target.value));
    setBaths(originalBaths);
  };

  const handleBathsChange = (e) => {
    setBaths(Number(e.target.value));
    setBeds(originalBeds);
  };

  const handleCityChange = (e) => {
    setSelectedCity(e.target.value);
  };

  return (
    <div className="results">
      <div className="range">
        <p>Estimated Lease Price:</p>
        <div className="range-bar">
          <div
            className="range-fill"
            style={{ width: "100%", backgroundColor: rangeFillColor }}
          >
            <div className="range-marker" style={{ left: "15%" }}>
              ${lowerBound}
            </div>
            <div className="range-marker" style={{ left: "85%" }}>
              ${upperBound}
            </div>
            <div
              className="range-marker prediction-marker"
              style={{ left: markerPosition }}
            >
              ${listPrice}
            </div>
          </div>
        </div>
        <p>
          The listed lease price is ${listPrice}, which is {explanation[0]} the
          predicted range. It is {explanation[1]} deal.
        </p>
      </div>

      <div>
        <div className="rectangle-outline">
          <p>
            Modify one attribute at a time to see changes in lease price range.
          </p>
          <div>
            <label>Bedrooms: {beds}</label>
            <input
              type="range"
              min={Math.max(1, originalBeds - 1)}
              max={Math.min(8, originalBeds + 1)}
              step="1"
              value={beds}
              onChange={handleBedsChange}
            />
          </div>

          <div>
            <label>Bathrooms: {baths}</label>
            <input
              type="range"
              min={Math.max(1, originalBaths - 0.5)}
              max={Math.min(5, originalBaths + 0.5)}
              step="0.5"
              value={baths}
              onChange={handleBathsChange}
            />
          </div>
          <p>New predicted range based on changes:</p>
          <p>
            ${roundToNearest25(newPrediction) - 125} to $
            {roundToNearest25(newPrediction) + 125}
          </p>
        </div>

        <div className="rectangle-outline">
          <p>
            Select a nearby city to view lease price range with same attributes.
          </p>
          {results.city_prediction.map((city, index) => (
            <div key={index}>
              <input
                type="radio"
                id={city[0]}
                name="city"
                value={city[0]}
                checked={selectedCity === city[0]}
                onChange={handleCityChange}
              />
              <label>{city[0]}</label>
            </div>
          ))}
          <p>New predicted range based on changes:</p>
          <p>
            ${roundToNearest25(cityPrediction) - 125} to $
            {roundToNearest25(cityPrediction) + 125}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Results;
