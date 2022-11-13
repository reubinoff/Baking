// base api requests

const BASE_URL = process.env.REACT_APP_BASE_URL;

function get_url(path) {
  return BASE_URL + "/" + path;
}

export function get(url, debug = false) {
  const URL = get_url(url);
  return fetch(URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    }})
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