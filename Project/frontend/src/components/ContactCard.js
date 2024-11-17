import React from "react";

function ContactCard({ contact }) {
  return (
    <div className="card max-w-md mx-auto my-4">
      <div className="flex items-center mb-4">
        <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white text-xl">
          {contact.firstName?.charAt(0)}
        </div>
        <div className="ml-4">
          <h3 className="text-xl font-semibold">{`${contact.firstName} ${contact.lastName}`}</h3>
          <p className="text-gray-600">{contact.title}</p>
        </div>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center text-gray-700">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <span>{contact.email}</span>
        </div>
        
        <div className="flex items-center text-gray-700">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>{contact.location}</span>
        </div>
        
        <div className="flex items-center text-gray-700">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <span>{contact.chatUsername}</span>
        </div>
      </div>
    </div>
  );
}

export default ContactCard;