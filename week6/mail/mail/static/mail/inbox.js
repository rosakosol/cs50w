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
    // Stop default behaviour after form submission which is to reload webpage
    preventDefault();

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

        // If successful then reload sent inbox
        load_mailbox('sent');
    });

  };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch(`/emails/${mailbox}`, {
    method: 'GET', 
  })

  // Turn response into JSON
  .then(response => response.json())

  .then(data => {
    const emailContainer = document.querySelector('#emails-view');

    // Print result
    console.log(data);

    data.forEach((email) => {
      // Create separate div for each email
      const emailElement = document.createElement('div');
      emailElement.classList.add('email-container');
      emailContainer.appendChild(emailElement);

      if ((!email.archived && mailbox === "inbox") || (!email.archived && mailbox === "sent") || (email.archived && mailbox === "archive"))  {
        // If in sent mailbox, do not show sender
        if (mailbox === "sent") {
          const recipientsElement = document.createElement('p');
          recipientsElement.classList.add('email-from-to');
          recipientsElement.textContent = `To: ${email.recipients}`;
          emailElement.appendChild(recipientsElement);
        } else {
          const senderElement = document.createElement('p');
          senderElement.classList.add('email-from-to');
          senderElement.textContent = `${email.sender}`;
          emailElement.appendChild(senderElement);
        }


        // Display subject
        const subjectElement = document.createElement('p');  
        subjectElement.classList.add('email-subject');
        subjectElement.textContent = `Subject: ${email.subject}`;
        emailElement.appendChild(subjectElement);
        
        // Display time stamp
        const timeElement = document.createElement('h5');  
        timeElement.textContent = email.timestamp;
        emailElement.appendChild(timeElement);

        // Add event listener to load email when clicked
        emailElement.addEventListener('click', () => load_single_email(email));
      }
    }); 
  });
}

// Load single email details when clicked and mark as read
function load_single_email(email) {
  // Show the email detail view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  const emailDetailContainer = document.querySelector('#single-email-view');
  // Clear view
  emailDetailContainer.innerHTML = ''

  // Mark email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  // Get the email and check if it was marked as read
  fetch(`/emails/${email.id}`, {
    method: 'GET',
  })

  .then(response => response.json())
  .then(data => {
    if (data.read) {
      console.log("Email marked as read.")
    } else {
      console.log("Error: Email could not be marked as read!")
    }
  })

  // Create separate div for each email
  const emailElement = document.createElement('div');
  emailElement.classList.add('single-email-container');
  emailDetailContainer.appendChild(emailElement);

  // Archive or unarchive email
  if (email.archived) {
    // Create unarchive button
    const unarchiveElement = document.createElement('button');
    unarchiveElement.classList.add('btn', 'btn-sm', 'btn-outline-primary');
    unarchiveElement.textContent = 'Unarchive';
    unarchiveElement.addEventListener('click', () => archive_email(email));
    emailElement.appendChild(unarchiveElement);
  } else {
    // Create archive button
    const archiveElement = document.createElement('button');
    archiveElement.classList.add('btn', 'btn-sm', 'btn-outline-primary');
    archiveElement.textContent = 'Archive';
    archiveElement.addEventListener('click', () => archive_email(email));
    emailElement.appendChild(archiveElement);
  }

  // Display time stamp
  const timeElement = document.createElement('h5');  
  timeElement.textContent = email.timestamp;
  emailElement.appendChild(timeElement);

  // Sender
  const senderElement = document.createElement('p');
  senderElement.classList.add('email-from-to');
  senderElement.textContent = `${email.sender}`;
  emailElement.appendChild(senderElement);

  // Recipients
  const recipientsElement = document.createElement('p');
  recipientsElement.classList.add('email-from-to');
  recipientsElement.textContent = `To: ${email.recipients}`;
  emailElement.appendChild(recipientsElement);

  // Display subject
  const subjectElement = document.createElement('p');  
  subjectElement.classList.add('email-subject');
  subjectElement.textContent = `Subject: ${email.subject}`;
  emailElement.appendChild(subjectElement);

  // Reply button
  const replyElement = document.createElement('button');
  replyElement.classList.add('btn', 'btn-sm', 'btn-outline-primary');
  replyElement.textContent = 'Reply';
  replyElement.addEventListener('click', () => reply_email(email));
  emailElement.appendChild(replyElement);

  // Body
  const bodyElement = document.createElement('p');
  bodyElement.classList.add('email-body');
  bodyElement.textContent = `${email.body}`;
  emailElement.appendChild(bodyElement);
}

function reply_email(email) {

}

function archive_email(email) {
  // Mark email as archived if unarchived
  if (!email.archived) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })

    fetch(`/emails/${email.id}`, {
      method: 'GET',
    })
  
    .then(response => response.json())
    .then(data => {
      if (data.archived) {
        console.log("Email marked as archived.")
      } else {
        console.log("Error: Email could not be marked as archived!")
      }
    })
  } 
  // Mark email as unarchived if archived
  else {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })

    fetch(`/emails/${email.id}`, {
      method: 'GET',
    })
  
    .then(response => response.json())
    .then(data => {
      if (!data.archived) {
        console.log("Email marked as unarchived.")
      } else {
        console.log("Error: Email could not be marked as unarchived!")
      }
    })
  }


  // Reload inbox
  load_mailbox('inbox');
}