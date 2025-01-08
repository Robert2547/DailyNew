export interface ApiError extends Error {
  type: "RATE_LIMIT" | "API_ERROR";
  isRateLimit?: boolean;
}

export const createRateLimitError = (
  message: string = "API rate limit exceeded"
): ApiError => {
  const error = new Error(message) as ApiError;
  error.type = "RATE_LIMIT";
  error.isRateLimit = true;
  return error;
};

export const createApiError = (message: string): ApiError => {
  const error = new Error(message) as ApiError;
  error.type = "API_ERROR";
  return error;
};

export const isRateLimitResponse = (data: any): boolean => {
  return (
    data?.Information?.includes("rate limit") ||
    data?.Note?.includes("API call frequency") ||
    data?.["Information"]?.includes("rate limit")
  );
};

export const handleApiError = (error: unknown): ApiError => {
  if ((error as ApiError).type) {
    return error as ApiError;
  }

  if (error instanceof Error) {
    if (error.message.includes("rate limit")) {
      return createRateLimitError();
    }
    return createApiError(error.message);
  }

  return createApiError("Unknown error occurred");
};
