import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertCircle, Clock, RefreshCcw, Home } from "lucide-react";

interface ErrorState {
  type: "RATE_LIMIT" | "API_ERROR";
  message?: string;
}

const APIError = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const errorState = location.state as ErrorState;

  const isRateLimit = errorState?.type === "RATE_LIMIT";

  const renderContent = () => {
    if (isRateLimit) {
      return (
        <>
          <div className="rounded-full bg-orange-100 p-3">
            <Clock className="h-8 w-8 text-orange-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            API Rate Limit Reached
          </h1>
          <p className="text-gray-600 max-w-md">
            We've hit our API rate limit. This typically happens when:
          </p>
          <ul className="text-left text-gray-600 space-y-2">
            <li className="flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-orange-500 flex-shrink-0 mt-0.5" />
              <span>
                You've made more than 5 requests per minute (free tier limit)
              </span>
            </li>
            <li className="flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-orange-500 flex-shrink-0 mt-0.5" />
              <span>You've reached the daily API call quota</span>
            </li>
          </ul>
        </>
      );
    }

    return (
      <>
        <div className="rounded-full bg-red-100 p-3">
          <AlertCircle className="h-8 w-8 text-red-600" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900">API Error</h1>
        <p className="text-gray-600 max-w-md">
          {errorState?.message || "An error occurred while fetching data"}
        </p>
      </>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
      <Card className="max-w-lg w-full p-6 space-y-6">
        <div className="flex flex-col items-center text-center space-y-4">
          {renderContent()}
        </div>

        <div className="space-y-4 pt-4">
          <p className="text-sm text-gray-500 text-center">
            {isRateLimit
              ? "Please wait a minute before trying again or return to the dashboard."
              : "Please try again or return to the dashboard."}
          </p>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => navigate(-1)}
            >
              <RefreshCcw className="mr-2 h-4 w-4" />
              Try Again
            </Button>

            <Button className="flex-1" onClick={() => navigate("/dashboard")}>
              <Home className="mr-2 h-4 w-4" />
              Go to Dashboard
            </Button>
          </div>
        </div>

        {isRateLimit && (
          <div className="pt-4 border-t">
            <p className="text-xs text-gray-500 text-center">
              Need higher rate limits? Consider upgrading to a premium API key
              or implementing local data caching.
            </p>
          </div>
        )}
      </Card>
    </div>
  );
};

export default APIError;
