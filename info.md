# Hotel Management System (HMS) - Working Features

## 1. User Authentication & Role-Based Access
- **Secure Authentication**: Built-in Django authentication for login and logout.
- **Role Control**: Distinct views and permissions for **Administrators/Staff** and **Regular Users**.
- **Admin Mixins**: Custom `AdminRequiredMixin` to protect administrative management views.

## 2. Hotel Management (Admin Only)
- **Hotel Registration**: Full CRUD support (Create, Read, Update, Delete) for hotel entries.
- **Detailed Profiles**: Store hotel names, locations, contact info, total rooms, and star ratings (1-5).
- **Media Support**: Support for hotel images to provide a rich visual experience.

## 3. Room Management (Admin Only)
- **Room Types**: Support for multiple room categories: Single, Double, and Deluxe.
- **Availability Tracking**: Real-time room availability status management.
- **Pricing Control**: Individual room pricing per night with validation checks.
- **Unique Identification**: Prevents duplicate room numbers within the same hotel.

## 4. Advance Booking System
- **Real-Time Booking**: Users can seamlessly book rooms for specific check-in and check-out dates.
- **Smart Validation**: Built-in checks to prevent past-date check-ins and invalid date sequences.
- **Overlap Prevention**: Automatic system check to prevent double-booking of the same room for overlapping dates.
- **Status Workflow**: Manage bookings through various states: *Booked*, *Checked-In*, *Checked-Out*, and *Cancelled*.
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
