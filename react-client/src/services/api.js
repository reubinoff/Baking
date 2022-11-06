// base api requests

const BASE_URL = process.env.BASE_URL || "http://localhost:8888";

function get_url(path) {
  return BASE_URL + "/" + path;
}

export function get(url, debug = false) {
  const URL = get_url(url);
  return fetch(URL)
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
