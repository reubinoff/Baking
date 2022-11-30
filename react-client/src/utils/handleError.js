
export default function handleError(res) {
  return Promise.all([res, res.text()])
    .then(([res, body]) => {
      if (!res.ok) {
        const responseError = {
          statusText: res.statusText,
          status: res.status,
          body: body,
        };
        throw responseError;
      }
      return [res, body];
    })
    .then(([res, text]) => {
      if (!text || text.length === 0) {
        return null;
      } else {
        try {
          return JSON.parse(text);
        } catch (e) {
          // Fallback if response is not json
          return text;
        }
      }
    });
}
