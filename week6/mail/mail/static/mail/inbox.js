document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector("#compose-form").onsubmit = function() {
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
  };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  console.log(mailbox)

  fetch(`/emails/${mailbox}`, {
    method: 'GET', 
  })

  // Turn response into JSON
  .then(response => response.json())

  .then(data => {
    // Handle the received emails
    console.log('Emails in', mailbox, ':', data);

    const emailContainer = document.querySelector('#emails-view');

    data.forEach((email) => {
      // Create separate div for each email
      const emailElement = document.createElement('div');
      emailElement.classList.add('email-container');
      emailContainer.appendChild(emailElement);

      // Display time stamp
      const timeElement = document.createElement('h5');  
      timeElement.textContent = email.timestamp;
      emailElement.appendChild(timeElement);

      // Display subject
      const subjectElement = document.createElement('h4');  
      subjectElement.textContent = `Subject: ${email.subject}`;
      emailElement.appendChild(subjectElement);

      // Display body
      const bodyElement = document.createElement('p');  
      bodyElement.textContent = `Body: ${email.body}`;
      emailElement.appendChild(bodyElement);

      // If in inbox mailbox, show sender an recipients
      if (mailbox === "inbox") {
        
      }

      // If in sent mailbox, do not show sender
      if (mailbox === "sent") {
        const recipientsElement = document.createElement('p');
        recipientsElement.textContent = `Recipients: ${email.recipients}`;
        emailElement.appendChild(recipientsElement);
      }




    });

    
  })



}