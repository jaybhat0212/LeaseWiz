import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import { ClipLoader } from "react-spinners";
import Results from "./Results";

const provinces = [
  "Alberta",
  "British Columbia",
  "Manitoba",
  "New Brunswick",
  "Newfoundland and Labrador",
  "Nova Scotia",
  "Ontario",
  "Prince Edward Island",
  "Quebec",
  "Saskatchewan",
];

const leaseTerms = ["Long Term", "Short Term"];
const types = ["House", "Condo", "Apartment", "Town House", "Basement"];

function App() {
  const [formData, setFormData] = useState({
    city: "",
    province: provinces[0],
    lease_term: leaseTerms[0],
    type: types[0],
    beds: 1,
    baths: 1,
    furnished: false,
    pets: false,
    sq_feet: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [listPrice, setListPrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name == "list_price") {
      setListPrice(value);
    } else {
      setFormData({
        ...formData,
        [name]: type === "checkbox" ? checked : value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("/predict", formData);
      setResults(response.data);
      console.log(response.data);
      setPrediction(response.data.predicted_price);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>LeaseWiz</h1>
      <h3>Helping you make the right decision choosing a good lease.</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>City</label>
          <input
            type="text"
            name="city"
            value={formData.city}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Province</label>
          <select
            name="province"
            value={formData.province}
            onChange={handleChange}
            required
          >
            {provinces.map((province) => (
              <option key={province} value={province}>
                {province}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Lease Term</label>
          <select
            name="lease_term"
            value={formData.lease_term}
            onChange={handleChange}
            required
          >
            {leaseTerms.map((term) => (
              <option key={term} value={term}>
                {term}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Type</label>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            {types.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Beds</label>
          <input
            type="range"
            name="beds"
            min="1"
            max="8"
            value={formData.beds}
            onChange={handleChange}
            required
          />
          <span>{formData.beds}</span>
        </div>

        <div className="form-group">
          <label>Baths</label>
          <input
            type="range"
            name="baths"
            min="1"
            max="5"
            step="0.5"
            value={formData.baths}
            onChange={handleChange}
            required
          />
          <span>{formData.baths}</span>
        </div>

        <div className="form-group">
          <label>Furnished</label>
          <input
            type="checkbox"
            name="furnished"
            checked={formData.furnished}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Pets</label>
          <input
            type="checkbox"
            name="pets"
            checked={formData.pets}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Square Footage</label>
          <input
            type="number"
            name="sq_feet"
            value={formData.sq_feet}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="list_price">List Price</label>{" "}
          <input
            type="number"
            name="list_price"
            value={formData.list_price}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit">Submit</button>
      </form>
      {loading ? (
        <div className="loading">
          <ClipLoader size={50} color={"#123abc"} loading={loading} />
        </div>
      ) : (
        prediction !== null && (
          <Results
            prediction={prediction}
            listPrice={listPrice}
            originalBeds={parseFloat(formData.beds)}
            originalBaths={parseFloat(formData.baths)}
            results={results}
          />
        )
      )}
    </div>
  );
}

export default App;
