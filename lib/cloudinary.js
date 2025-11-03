import { v2 as cloudinary } from "cloudinary";

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

export async function uploadToCloudinary(fileBase64, filename) {
  try {
    const result = await cloudinary.uploader.upload(fileBase64, {
      folder: "patient_reports",
      public_id: filename,
      resource_type: "auto", // works for PDFs, images, etc.
    });
    return result.secure_url; // this is the file’s public URL
  } catch (err) {
    console.error("Cloudinary upload failed:", err);
    throw new Error("Upload failed");
  }
}
