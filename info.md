# Hotel Management System (HMS) - Working Features

## 1. User Authentication & Role-Based Access
- **Secure Authentication**: Built-in Django authentication for login and logout.
- **Role Control**: Distinct views and permissions for **Administrators/Staff** and **Regular Users**.
- **Admin Mixins**: Custom `AdminRequiredMixin` to protect administrative management views.
- **User Management (Staff Only)**: Dedicated dashboard to list all registered user accounts and manage account deletion.

## 2. Hotel Management (Admin Only)
- **Hotel Registration**: Full CRUD support (Create, Read, Update, Delete) for hotel entries.
- **Detailed Profiles**: Store names, locations, contact info, total rooms, star ratings (1-5), and **comprehensive descriptions**.
- **Multimedia & Contacts**: Support for property images, direct contact emails, and official websites.
- **Amenities Tracking**: Manage and display a curated list of property amenities (WiFi, Pool, etc.).

## 3. Room Management (Admin Only)
- **Room Types**: Support for multiple room categories: Single, Double, and Deluxe.
- **Availability Tracking**: Real-time room availability status management.
- **Rich Media**: Dedicated image support and detailed descriptions for individual rooms.
- **Size Tracking**: Prominent display of room dimensions in square meters (sqm).
- **Medium Premium Layout**: Balanced 3-per-row discovery grid for a spacious luxury aesthetic.
- **Pricing Control**: Individual room pricing per night with validation checks.
- **Unique Identification**: Prevents duplicate room numbers within the same hotel.

## 4. Advance Booking System
- **Real-Time Booking**: Users can seamlessly book rooms for specific check-in and check-out dates.
- **Smart Validation**: Built-in checks to prevent past-date check-ins and invalid date sequences.
- **Overlap Prevention**: Automatic system check to prevent double-booking of the same room for overlapping dates.
- **Status Workflow**: Manage bookings through various states: *Booked*, *Checked-In*, *Checked-Out*, and *Cancelled*, with visual indicators.
- **Premium Dashboard**: Real-time summary statistics for active, completed, and cancelled reservations.
- **Automatic Transitions**: Room availability automatically updates based on booking status changes or deletion.

## 5. Billing & Invoicing
- **Automated Costing**: Precise total amount calculation based on stay duration (minimum 1-night charge).
- **Bill Summaries**: Detailed billing view for each booking, restricted to the booking owner and staff members.
- **Payment Linkage**: Underlying infrastructure for tracking payment methods and transaction dates.

## 6. User Profile Enhancements
- **Profile Customization**: Users can upload and manage their own profile photos.
- **Unified Booking History**: A central profile dashboard listing all past and upcoming stays.
- **Integrated Invoicing**: Quick access to digital invoices/bills directly from the booking history.
- **Loyalty Program**: Automatic point accumulation (10 points per night stayed) awarded upon checkout.

## 7. Dynamic Dashboard & Statistics
- **Real-Time Stats**: At-a-glance view of system-wide metrics: Total Hotels, Rooms, and Bookings.
- **Personalized Views**: Regular users see a personalized dashboard with their own booking history and counts.

## 8. Premium User Interface
- **Professional Navigation**: Clean, modern navbar with a unified user dropdown for Profile, Management, and Logout.
- **Micro-Animations**: Smooth transitions and hover effects throughout the application for a premium feel.
- **Improved UX**: Clear text-labeled actions in booking management for better identifying administrative tasks.
- **Premium Authentication**: A stunning, modern login interface with industrial-grade aesthetic and animations.
