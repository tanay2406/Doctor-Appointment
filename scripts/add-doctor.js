// scripts/add-doctor.js
// import dotenv from "dotenv";
// import path from "path";
// import { db } from "../lib/prisma.js";
// import { v4 as uuidv4 } from "uuid";

// // Load .env
// dotenv.config({ path: path.resolve("./.env") });

// // List of specializations
// const specializations = [
//   "General Medicine",
//   "Cardiology",
//   "Dermatology",
//   "Endocrinology",
//   "Gastroenterology",
//   "Neurology",
//   "Obstetrics & Gynecology",
//   "Oncology",
//   "Ophthalmology",
//   "Orthopedics",
//   "Pediatrics",
//   "Psychiatry",
//   "Pulmonology",
//   "Radiology",
//   "Urology",
//   "Other",
// ];

// // Some random names
// const firstNames = [
//   "Robert", "John", "Michael", "William", "David",
//   "Mary", "Patricia", "Linda", "Barbara", "Elizabeth",
//   "James", "Jennifer", "Susan", "Jessica", "Daniel",
// ];

// const lastNames = [
//   "Smith", "Johnson", "Williams", "Brown", "Jones",
//   "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
// ];

// // Helper to pick random array element
// function randomItem(arr) {
//   return arr[Math.floor(Math.random() * arr.length)];
// }

// // Generate 3 doctors per specialization
// function generateDoctors() {
//   const doctors = [];

//   specializations.forEach((specialty) => {
//     for (let i = 1; i <= 3; i++) {
//       const firstName = randomItem(firstNames);
//       const lastName = randomItem(lastNames);
//       const name = `${firstName} ${lastName}`;
//       const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}${i}@example.com`;

//       doctors.push({
//         clerkUserId: uuidv4(),
//         email,
//         name,
//         role: "DOCTOR",
//         specialty,
//         experience: Math.floor(Math.random() * 15) + 1, // 1–15 years
//         description: `Dr. ${name} is an experienced ${specialty} specialist.`,
//         verificationStatus: "VERIFIED",
//         credits: 0,
//       });
//     }
//   });

//   return doctors;
// }

// async function main() {
//   const doctors = generateDoctors();

//   for (const doc of doctors) {
//     try {
//       const created = await db.user.create({
//         data: doc,
//       });
//       console.log(`✅ Created doctor: ${created.name} (${created.specialty})`);
//     } catch (err) {
//       console.error("❌ Error creating doctor:", err.message);
//     }
//   }

//   console.log("🎉 All doctors added!");
//   process.exit(0);
// }

// main();
