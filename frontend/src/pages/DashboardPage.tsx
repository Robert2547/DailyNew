import { TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const DashboardPage = () => {
  return (
    <>
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-400 rounded-lg shadow-lg p-6 mb-8 text-white">
        <h1 className="text-3xl font-bold">Welcome back, John! 👋</h1>
        <p className="mt-2 text-blue-50">
          Here's what's happening with your watched companies today
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[
          { title: "Tracked Companies", value: "12", trend: "+2%" },
          { title: "Today's News", value: "89", trend: "+14%" },
          { title: "Market Sentiment", value: "70%", trend: "+5%" },
        ].map((stat, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                {stat.title}
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-sm text-green-500 flex items-center mt-1">
                <TrendingUp className="h-4 w-4 mr-1" />
                {stat.trend} from yesterday
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Rest of the components remain the same */}
        {/* Watchlist */}
        <Card>{/* Watchlist content remains the same */}</Card>

        {/* News Feed */}
        <Card>{/* News Feed content remains the same */}</Card>

        {/* Sentiment Analysis */}
        <Card>{/* Sentiment Analysis content remains the same */}</Card>
      </div>
    </>
  );
};

export default DashboardPage;
