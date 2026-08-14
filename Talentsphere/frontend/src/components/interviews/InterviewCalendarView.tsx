import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  Plus,
  Video,
  MoreHorizontal,
  Grid,
  Filter,
  Check,
  Clock,
  User,
  ExternalLink,
  MapPin
} from 'lucide-react';
import { useNotification } from '../../context/NotificationContext';

export const InterviewCalendarView: React.FC = () => {
  const { interviews, addInterview } = useOrganization();
  const { showSuccess } = useNotification();

  // Selected date state (defaults to August 2026 matching user's image)
  const [selectedYear] = useState(2026);
  const [selectedMonth] = useState(7); // August (0-indexed)
  const [activeDay, setActiveDay] = useState(10); // August 10, 2026

  // View state
  const [viewMode, setViewMode] = useState<'Day' | 'Work Week' | 'Week' | 'Month'>('Week');
  const [myCalendars, setMyCalendars] = useState({
    calendar: true,
    interviews: true,
    holidays: false,
  });

  // Modal state for booking a new meeting
  const [isBookModalOpen, setIsBookModalOpen] = useState(false);
  const [newMeeting, setNewMeeting] = useState({
    candidateName: '',
    roundName: 'Technical Interview',
    date: '2026-08-10',
    time: '10:00',
    duration: 60,
    interviewerName: 'Harsh Shirsath',
    location: 'Microsoft Teams Meeting',
  });

  // Generate days for mini-calendar (August 2026)
  const getDaysInMonth = (year: number, month: number) => {
    const date = new Date(year, month, 1);
    const days = [];
    // Pad for starting day of week
    const startDay = date.getDay(); // 0 is Sunday
    const prevMonthDays = new Date(year, month, 0).getDate();
    
    for (let i = startDay - 1; i >= 0; i--) {
      days.push({ day: prevMonthDays - i, currentMonth: false });
    }
    
    const totalDays = new Date(year, month + 1, 0).getDate();
    for (let i = 1; i <= totalDays; i++) {
      days.push({ day: i, currentMonth: true });
    }
    
    // Pad end
    const remaining = 42 - days.length;
    for (let i = 1; i <= remaining; i++) {
      days.push({ day: i, currentMonth: false });
    }
    
    return days;
  };

  const miniCalendarDays = getDaysInMonth(selectedYear, selectedMonth);

  // Time grid rows: 08:00 to 23:00
  const timeHours = Array.from({ length: 16 }, (_, i) => i + 8);

  // 7 Days of the active week (August 9, 2026 - August 15, 2026)
  const weekDays = [
    { num: 9, name: 'Sunday' },
    { num: 10, name: 'Monday' },
    { num: 11, name: 'Tuesday' },
    { num: 12, name: 'Wednesday' },
    { num: 13, name: 'Thursday' },
    { num: 14, name: 'Friday' },
    { num: 15, name: 'Saturday' }
  ];

  // Helper to place meetings in slots
  const getMeetingsForDayAndTime = (dayNum: number, hour: number) => {
    // Return custom seeded/saved interviews mapping to this day
    const mapped = interviews.filter((int) => {
      // Parse day from interview date
      const intDay = parseInt(int.date?.split('-')[2] || '10', 10);
      const intHour = parseInt(int.time?.split(':')[0] || '10', 10);
      return intDay === dayNum && intHour === hour;
    });
    return mapped;
  };

  const handleBookMeeting = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMeeting.candidateName) return;

    addInterview({
      candidateId: `cand-${Date.now()}`,
      candidateName: newMeeting.candidateName,
      candidateAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      jobId: 'job-1',
      jobTitle: 'Software Architect',
      roundName: newMeeting.roundName,
      interviewerName: newMeeting.interviewerName,
      interviewerRole: 'Technical Lead',
      date: newMeeting.date,
      time: newMeeting.time,
      durationMinutes: newMeeting.duration,
      location: newMeeting.location,
      meetingLink: 'https://teams.microsoft.com/l/meetup-join/example',
      status: 'Scheduled'
    });

    showSuccess('Meeting Booked', `Interview scheduled for ${newMeeting.candidateName}`);
    setIsBookModalOpen(false);
    setNewMeeting({
      candidateName: '',
      roundName: 'Technical Interview',
      date: '2026-08-10',
      time: '10:00',
      duration: 60,
      interviewerName: 'Harsh Shirsath',
      location: 'Microsoft Teams Meeting',
    });
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full text-left animate-fade-in text-zinc-950 dark:text-zinc-100 min-h-[calc(100vh-140px)]">
      {/* 1. LEFT SIDEBAR PANEL (Microsoft Teams Mini Navigation) */}
      <div className="w-full lg:w-60 shrink-0 space-y-6 bg-zinc-50 dark:bg-zinc-950/60 p-4 rounded-3xl border border-zinc-200 dark:border-zinc-800 shadow-md">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold tracking-tight">Calendar</h2>
        </div>

        {/* Mini Calendar Card */}
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs px-1">
            <span className="font-bold font-sans">August 2026</span>
            <div className="flex items-center gap-1.5">
              <button className="p-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 transition">
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <button className="p-1 rounded hover:bg-zinc-200 dark:hover:bg-zinc-800 transition">
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Mini Calendar Grid */}
          <div className="grid grid-cols-7 gap-y-2 text-center text-[10px] font-sans">
            {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, i) => (
              <span key={i} className="text-zinc-400 font-semibold">{d}</span>
            ))}
            {miniCalendarDays.map((d, i) => {
              const isSelectedWeek = d.currentMonth && d.day >= 9 && d.day <= 15;
              const isActiveDay = d.currentMonth && d.day === activeDay;

              return (
                <button
                  key={i}
                  onClick={() => d.currentMonth && setActiveDay(d.day)}
                  className={`w-6 h-6 mx-auto rounded-full flex items-center justify-center font-medium transition ${
                    !d.currentMonth ? 'text-zinc-300 dark:text-zinc-700' : ''
                  } ${
                    isSelectedWeek ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400' : ''
                  } ${
                    isActiveDay ? '!bg-indigo-600 !text-white font-bold' : 'hover:bg-zinc-200 dark:hover:bg-zinc-800'
                  }`}
                >
                  {d.day}
                </button>
              );
            })}
          </div>
        </div>

        <button className="w-full flex items-center justify-center gap-2 py-2 rounded-xl border border-zinc-300 dark:border-zinc-800 text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-900 transition">
          <Plus className="w-3.5 h-3.5" /> Add calendar
        </button>

        {/* My Calendars Filter */}
        <div className="space-y-3 pt-2">
          <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">My Calendars</span>
          <div className="space-y-2 text-xs">
            <label className="flex items-center gap-2.5 cursor-pointer">
              <input
                type="checkbox"
                checked={myCalendars.calendar}
                onChange={() => setMyCalendars(prev => ({ ...prev, calendar: !prev.calendar }))}
                className="w-4 h-4 rounded border-zinc-300 dark:border-zinc-700 text-indigo-600 focus:ring-indigo-500 bg-white dark:bg-black"
              />
              <span className="font-medium">Primary Calendar</span>
            </label>
            <label className="flex items-center gap-2.5 cursor-pointer">
              <input
                type="checkbox"
                checked={myCalendars.interviews}
                onChange={() => setMyCalendars(prev => ({ ...prev, interviews: !prev.interviews }))}
                className="w-4 h-4 rounded border-zinc-300 dark:border-zinc-700 text-indigo-600 focus:ring-indigo-500 bg-white dark:bg-black"
              />
              <span className="font-medium">AI Interviews</span>
            </label>
          </div>
        </div>
      </div>

      {/* 2. MAIN CALENDAR GRID VIEW (Microsoft Teams Style Week View) */}
      <div className="flex-1 flex flex-col bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800/80 rounded-3xl shadow-xl overflow-hidden">
        
        {/* Toolbar Header Row */}
        <div className="p-4 border-b border-zinc-200 dark:border-zinc-800 flex flex-wrap items-center justify-between gap-4 bg-zinc-50/50 dark:bg-zinc-900/20">
          {/* Left Controls */}
          <div className="flex items-center gap-3">
            <button className="p-2 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-800 transition">
              <Grid className="w-4 h-4 text-zinc-500" />
            </button>
            <button
              onClick={() => setActiveDay(10)}
              className="px-3 py-1.5 rounded-lg border border-zinc-300 dark:border-zinc-800 text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-900 transition"
            >
              Today
            </button>
            <div className="flex items-center gap-1">
              <button className="p-2 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-800 transition">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-800 transition">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <span className="text-sm font-bold tracking-tight px-1 font-sans">
              09–15 August, 2026
            </span>
          </div>

          {/* Right Controls */}
          <div className="flex items-center gap-2">
            {/* View Selector Dropdown */}
            <select
              value={viewMode}
              onChange={(e) => setViewMode(e.target.value as any)}
              className="px-3 py-1.5 rounded-lg border border-zinc-300 dark:border-zinc-800 text-xs font-semibold bg-white dark:bg-zinc-900 focus:outline-none"
            >
              <option value="Day">Day</option>
              <option value="Work Week">Work Week</option>
              <option value="Week">Week</option>
              <option value="Month">Month</option>
            </select>

            <button className="p-2 rounded-lg border border-zinc-300 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition" title="Filter">
              <Filter className="w-4 h-4 text-zinc-500" />
            </button>

            <button className="p-2 rounded-lg border border-zinc-300 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 transition">
              <MoreHorizontal className="w-4 h-4 text-zinc-500" />
            </button>

            <button className="px-4 py-2 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-xs font-bold hover:bg-zinc-200 dark:hover:bg-zinc-700 transition flex items-center gap-1.5 text-zinc-850 dark:text-zinc-150 border border-zinc-300 dark:border-zinc-750">
              <Video className="w-4 h-4 text-zinc-500" /> Meet now
            </button>

            <button
              onClick={() => setIsBookModalOpen(true)}
              className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-md shadow-indigo-600/10 active:scale-95"
            >
              <Plus className="w-4 h-4" /> New meeting
            </button>
          </div>
        </div>

        {/* Weekly Header Column Labels */}
        <div className="grid grid-cols-8 border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50/30 dark:bg-zinc-900/10">
          {/* Pad for Time Axis */}
          <div className="border-r border-zinc-200 dark:border-zinc-800/80 p-3 text-center text-[10px] font-bold text-zinc-400 font-sans uppercase tracking-wider">
            Time
          </div>
          {weekDays.map((day) => {
            const isToday = day.num === activeDay;
            return (
              <div
                key={day.num}
                className={`p-3 border-r border-zinc-200 dark:border-zinc-800 text-center relative flex flex-col items-center justify-center transition-colors ${
                  isToday ? 'bg-indigo-500/5' : ''
                }`}
              >
                {/* Active Top Bar Indicator */}
                {isToday && (
                  <div className="absolute top-0 left-0 right-0 h-1 bg-indigo-600" />
                )}
                <span className={`text-[13px] font-extrabold ${isToday ? 'text-indigo-600 dark:text-indigo-400' : 'text-zinc-800 dark:text-zinc-200'}`}>
                  {String(day.num).padStart(2, '0')}
                </span>
                <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500 font-sans mt-0.5">
                  {day.name}
                </span>
              </div>
            );
          })}
        </div>

        {/* Main Calendar Body Grid (Hours Scroll Area) */}
        <div className="flex-1 overflow-y-auto max-h-[600px] relative custom-scrollbar">
          
          {/* Horizontal Red Line showing Current Time Line */}
          <div className="absolute left-0 right-0 border-t-2 border-dashed border-red-500 z-20 pointer-events-none" style={{ top: '65%' }}>
            <div className="absolute -left-1 -top-1.5 w-3 h-3 rounded-full bg-red-500" />
          </div>

          <div className="grid grid-cols-8 divide-y divide-zinc-200 dark:divide-zinc-800/50">
            {timeHours.map((hour) => (
              <React.Fragment key={hour}>
                {/* Time Axis Cell */}
                <div className="p-3 border-r border-zinc-200 dark:border-zinc-800 text-center font-mono text-[10px] font-bold text-zinc-400 dark:text-zinc-600 h-[80px] flex items-start justify-center">
                  {String(hour).padStart(2, '0')}:00
                </div>

                {/* 7 Day Column Slots for this hour */}
                {weekDays.map((day) => {
                  const cellMeetings = getMeetingsForDayAndTime(day.num, hour);

                  return (
                    <div
                      key={day.num}
                      onClick={() => {
                        setNewMeeting(prev => ({
                          ...prev,
                          date: `2026-08-${String(day.num).padStart(2, '0')}`,
                          time: `${String(hour).padStart(2, '0')}:00`
                        }));
                        setIsBookModalOpen(true);
                      }}
                      className="border-r border-zinc-200 dark:border-zinc-800 h-[80px] p-1.5 relative group hover:bg-zinc-50/50 dark:hover:bg-zinc-900/30 transition cursor-pointer"
                    >
                      {/* Plus icon on hover for booking */}
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 pointer-events-none transition duration-150">
                        <Plus className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                      </div>

                      {/* Display Meeting Cards if present */}
                      {cellMeetings.map((meet: any, mIdx) => (
                        <div
                          key={meet.id || mIdx}
                          onClick={(e) => {
                            e.stopPropagation();
                            showSuccess('Meeting Details', `${meet.candidateName} - Organised by ${meet.interviewerName}`);
                          }}
                          className="absolute inset-x-1.5 top-1.5 bottom-1.5 p-2 rounded-lg bg-indigo-500/10 dark:bg-indigo-900/30 border-l-4 border-indigo-600 dark:border-indigo-400 text-left flex flex-col justify-between overflow-hidden shadow-sm hover:shadow-md transition group-hover:scale-[1.02]"
                        >
                          <div className="space-y-0.5">
                            <h4 className="text-[10px] font-bold text-zinc-800 dark:text-white truncate font-sans tracking-tight">
                              {meet.candidateName}
                            </h4>
                            <p className="text-[9px] font-semibold text-indigo-700 dark:text-indigo-300 truncate">
                              {meet.roundName}
                            </p>
                          </div>
                          
                          <div className="flex items-center justify-between text-[8px] text-zinc-400 dark:text-zinc-500 pt-1 font-mono">
                            <span className="truncate flex items-center gap-0.5">
                              <User className="w-2 h-2" /> {meet.interviewerName}
                            </span>
                            <span className="shrink-0 flex items-center gap-0.5">
                              <Video className="w-2.5 h-2.5 text-indigo-500" /> join
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  );
                })}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>

      {/* 3. NEW MEETING BOOKING MODAL */}
      {isBookModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white dark:bg-zinc-950 p-6 text-left space-y-5 border border-zinc-200 dark:border-zinc-800 shadow-2xl">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-zinc-900 dark:text-white flex items-center gap-2">
                <CalendarIcon className="w-5 h-5 text-indigo-600" /> Book Interview Slot
              </h3>
              <button
                onClick={() => setIsBookModalOpen(false)}
                className="text-zinc-400 hover:text-zinc-900 dark:hover:text-white text-xs font-semibold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleBookMeeting} className="space-y-4 text-xs">
              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                  Candidate Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. John Doe"
                  value={newMeeting.candidateName}
                  onChange={(e) => setNewMeeting(prev => ({ ...prev, candidateName: e.target.value }))}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-zinc-300 dark:border-zinc-800 dark:bg-black dark:text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                    Date
                  </label>
                  <input
                    type="date"
                    required
                    value={newMeeting.date}
                    onChange={(e) => setNewMeeting(prev => ({ ...prev, date: e.target.value }))}
                    className="w-full px-3 py-2 rounded-xl border border-zinc-300 dark:border-zinc-800 dark:bg-black dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                    Start Time
                  </label>
                  <input
                    type="time"
                    required
                    value={newMeeting.time}
                    onChange={(e) => setNewMeeting(prev => ({ ...prev, time: e.target.value }))}
                    className="w-full px-3 py-2 rounded-xl border border-zinc-300 dark:border-zinc-800 dark:bg-black dark:text-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                  Interviewer (Hiring Manager)
                </label>
                <input
                  type="text"
                  required
                  value={newMeeting.interviewerName}
                  onChange={(e) => setNewMeeting(prev => ({ ...prev, interviewerName: e.target.value }))}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-zinc-300 dark:border-zinc-800 dark:bg-black dark:text-white"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsBookModalOpen(false)}
                  className="px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-800 text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-900 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition shadow-md"
                >
                  Save Meeting
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
