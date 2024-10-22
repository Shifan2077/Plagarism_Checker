const url = 'http://localhost:3000/api/submissions';
const tableBody = document.getElementById('tableBody');

// Fetch data from the API
fetch(url)
  .then(response => response.json())
  .then(submissions => {
    // Loop through the submissions and create table rows
    submissions.forEach(submission => {
      const row = tableBody.insertRow();
      const idCell = row.insertCell();
      const usernameCell = row.insertCell();
      const emailCell = row.insertCell();
      const mobileCell = row.insertCell();
      const educationCell = row.insertCell();
      const hoursCell = row.insertCell();
      const pagesCell = row.insertCell();
      const paymentPathCell = row.insertCell();
      const pdfPathCell = row.insertCell();

      idCell.textContent = submission._id;
      usernameCell.textContent = submission.username;
      emailCell.textContent = submission.email;
      mobileCell.textContent = submission.mobile;
      educationCell.textContent = submission.education;
      hoursCell.textContent = submission.hours;
      pagesCell.textContent = submission.pages;
      paymentPathCell.textContent = submission.payment_path;
      pdfPathCell.textContent = submission.pdf_path;
    });
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });