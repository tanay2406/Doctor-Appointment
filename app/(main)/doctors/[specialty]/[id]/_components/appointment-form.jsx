"use client";

import { useState, useEffect } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { format } from "date-fns";
import { Loader2, Clock, ArrowLeft, Calendar, CreditCard, Upload } from "lucide-react";
import { bookAppointment } from "@/actions/appointments";
import { toast } from "sonner";
import useFetch from "@/hooks/use-fetch";

export function AppointmentForm({ doctorId, slot, onBack, onComplete }) {
  const [description, setDescription] = useState("");
  const [appointmentType, setAppointmentType] = useState("offline");

  // --- Personal info ---
  const [personal, setPersonal] = useState({
    name: "",
    gender: "",
    age: "",
    bloodGroup: "",
  });

  // --- Medical info ---
  const [medical, setMedical] = useState({
    symptoms: "",
    history: "",
    ongoingTreatment: "",
    medications: "",
    allergies: "",
    chronicConditions: "",
  });

  // --- Report upload ---
  const [reports, setReports] = useState([{ reportName: "", file: null }]);

  const { loading, data, fn: submitBooking } = useFetch(bookAppointment);

  const handlePersonalChange = (e) =>
    setPersonal({ ...personal, [e.target.name]: e.target.value });

  const handleMedicalChange = (e) =>
    setMedical({ ...medical, [e.target.name]: e.target.value });

  const handleReportChange = (index, field, value) => {
    const newReports = [...reports];
    newReports[index][field] = value;
    setReports(newReports);
  };

  const addReportField = () => setReports([...reports, { reportName: "", file: null }]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("doctorId", doctorId);
    formData.append("startTime", slot.startTime);
    formData.append("endTime", slot.endTime);
    formData.append("description", description);
    formData.append("appointmentType", appointmentType);

    // Combine personal + medical info
    const fullMedicalForm = { ...personal, ...medical };
    formData.append("medicalForm", JSON.stringify(fullMedicalForm));

    // Attach report files
    const reportFilesBase64 = await Promise.all(
      reports
        .filter((r) => r.file)
        .map(async (r) => ({
          filename: r.reportName || r.file.name,
          data: await fileToBase64(r.file),
        }))
    );

    formData.append("reportFilesBase64", JSON.stringify(reportFilesBase64));

    await submitBooking(formData);
  };

  const fileToBase64 = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

  useEffect(() => {
    if (data && data.success) {
      toast.success("Appointment booked successfully!");
      onComplete();
    }
  }, [data]);

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* --- Appointment Info --- */}
      <div className="bg-muted/20 p-4 rounded-lg border border-emerald-900/20 space-y-3">
        <div className="flex items-center">
          <Calendar className="h-5 w-5 text-emerald-400 mr-2" />
          <span className="text-white font-medium">
            {format(new Date(slot.startTime), "EEEE, MMMM d, yyyy")}
          </span>
        </div>
        <div className="flex items-center">
          <Clock className="h-5 w-5 text-emerald-400 mr-2" />
          <span className="text-white">{slot.formatted}</span>
        </div>
        <div className="flex items-center">
          <CreditCard className="h-5 w-5 text-emerald-400 mr-2" />
          <span className="text-muted-foreground">
            Cost: <span className="text-white font-medium">2 credits</span>
          </span>
        </div>
      </div>

      {/* --- Appointment Type --- */}
      <div className="space-y-2">
        <Label>Select Appointment Type</Label>
        <div className="flex space-x-4">
          {["offline", "virtual"].map((type) => (
            <label key={type} className="flex items-center space-x-2">
              <input
                type="radio"
                name="appointmentType"
                value={type}
                checked={appointmentType === type}
                onChange={(e) => setAppointmentType(e.target.value)}
              />
              <span className="capitalize">{type}</span>
            </label>
          ))}
        </div>
      </div>

      {/* --- Personal Details --- */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-emerald-500">Personal Details</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <input
              name="name"
              value={personal.name}
              onChange={handlePersonalChange}
              className="border rounded-md w-full p-2"
              required
            />
          </div>
          <div>
            <Label htmlFor="age">Age</Label>
            <input
              name="age"
              type="number"
              value={personal.age}
              onChange={handlePersonalChange}
              className="border rounded-md w-full p-2"
              required
            />
          </div>
          <div>
            <Label>Gender</Label>
            <div className="flex space-x-4 mt-1">
              {["Male", "Female", "Other"].map((g) => (
                <label key={g} className="flex items-center space-x-2">
                  <input
                    type="radio"
                    name="gender"
                    value={g}
                    checked={personal.gender === g}
                    onChange={handlePersonalChange}
                    required
                  />
                  <span>{g}</span>
                </label>
              ))}
            </div>
          </div>
          <div>
            <Label htmlFor="bloodGroup">Blood Group</Label>
            <input
              name="bloodGroup"
              value={personal.bloodGroup}
              onChange={handlePersonalChange}
              className="border rounded-md w-full p-2"
              required
            />
          </div>
        </div>
      </div>

      {/* --- Medical Details --- */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-emerald-500">Medical Details</h3>
        {[
          ["symptoms", "Symptoms"],
          ["history", "Past Medical History"],
          ["ongoingTreatment", "Ongoing Treatment"],
          ["medications", "Medications"],
          ["allergies", "Allergies"],
          ["chronicConditions", "Chronic Conditions"],
        ].map(([key, label]) => (
          <div key={key}>
            <Label htmlFor={key}>{label}</Label>
            <Textarea
              name={key}
              value={medical[key]}
              onChange={handleMedicalChange}
              className="bg-background border-emerald-900/20 h-20"
            />
          </div>
        ))}
      </div>

      {/* --- Upload Reports --- */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-emerald-500">Upload Reports</h3>
        {reports.map((r, i) => (
          <div key={i} className="flex items-center space-x-4">
            <input
              type="text"
              placeholder="Report Name (e.g., BP Report)"
              value={r.reportName}
              onChange={(e) => handleReportChange(i, "reportName", e.target.value)}
              className="border rounded-md w-1/2 p-2"
            />
            <input
              type="file"
              onChange={(e) => handleReportChange(i, "file", e.target.files[0])}
            />
          </div>
        ))}
        <Button
          type="button"
          variant="outline"
          onClick={addReportField}
          className="flex items-center space-x-2 border-emerald-900/30"
        >
          <Upload className="h-4 w-4" />
          <span>Add Another Report</span>
        </Button>
      </div>

      {/* --- Description --- */}
      <div className="space-y-2">
        <Label htmlFor="description">Additional Description (optional)</Label>
        <Textarea
          id="description"
          placeholder="Anything else you'd like to add?"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="bg-background border-emerald-900/20 h-24"
        />
      </div>

      {/* --- Buttons --- */}
      <div className="flex justify-between pt-2">
        <Button
          type="button"
          variant="outline"
          onClick={onBack}
          disabled={loading}
          className="border-emerald-900/30"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Change Time Slot
        </Button>
        <Button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 hover:bg-emerald-700"
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Booking...
            </>
          ) : (
            "Confirm Booking"
          )}
        </Button>
      </div>
    </form>
  );
}

