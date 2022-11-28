// base api requests
import { useEffect, useState, useCallback } from "react";

const BASE_URL = process.env.REACT_APP_BASE_URL;

function get_url(path) {
  return BASE_URL + "/" + path;
}

const request = async (url, options) => {
  const response = await fetch(url, options);
  if (!response.ok) {
    console.error("FAILED!!");
  }
  const json = await response.json();
  console.log(json);
  return json;
};



export function get(url) {
  const URL = get_url(url);
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    }}
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState(null);

  const sendQuery = useCallback(async () => {
    try {
      await setLoading(true);
      await setError(false);
      const res = await request(URL, options);
      await setData(res);
      setLoading(false);
    } catch (err) {
      setError(err);
    }
  }, [URL, options]);

  useEffect(() => {
    sendQuery(URL);
  }, [url]);

  return { loading, error, data };
}


export function post (url, data, debug = false) {
  const URL = get_url(url);
  return fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if(!response.ok){
        console.error("FAILED!!");
      }

      return response.json().then((data) => {
        if (debug) {
          console.log(data);
        }
        return data;
      });
    })
    .catch((err) => {
      console.error(err);
    });
}