export async function requestJson(url, options, onError) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
    return data;
  } catch (error) {
    onError(error.message || 'The server is unavailable. Please try again.');
    return null;
  }
}
