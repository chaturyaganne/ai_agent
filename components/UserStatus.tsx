"use client";

interface UserStatusProps {
  status: {
    username: string;
    onboarding_step: number;
    onboarding_complete: boolean;
    created_at: string;
    last_message_at: string;
  } | null;
}

export default function UserStatus({ status }: UserStatusProps) {
  if (!status) {
    return (
      <div className="bg-white bg-opacity-95 rounded-lg shadow-lg p-6">
        <p className="text-gray-500">Loading status...</p>
      </div>
    );
  }

  const progress = (status.onboarding_step / 7) * 100;

  return (
    <div className="bg-white bg-opacity-95 rounded-lg shadow-lg p-6 sticky top-8">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Your Progress</h2>

      <div className="space-y-4">
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">
            Day {status.onboarding_step} of 7
          </p>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-indigo-600 to-purple-600 h-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">{Math.round(progress)}% Complete</p>
        </div>

        <div className="pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-600">
            <strong>Member:</strong> {status.username}
          </p>
          <p className="text-xs text-gray-600 mt-1">
            <strong>Started:</strong> {new Date(status.created_at).toLocaleDateString()}
          </p>
          {status.onboarding_complete && (
            <div className="mt-4 p-3 bg-green-100 rounded-lg">
              <p className="text-sm font-medium text-green-800">🎉 Onboarding Complete!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
