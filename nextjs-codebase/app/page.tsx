import { Button } from "@/components/ui/button";
import AuthButton from "../components/AuthButton";
import { createClient } from "@/utils/supabase/server";


export default async function Index() {
  const canInitSupabaseClient = () => {
    // This function is just for the interactive tutorial.
    // Feel free to remove it once you have Supabase connected.
    try {
      createClient();
      return true;
    } catch (e) {
      return false;
    }
  };

  const isSupabaseConnected = canInitSupabaseClient();

  return (
    <div className="flex-1 w-full flex flex-col gap-20 items-center">
      <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
        <div className="w-full max-w-4xl flex justify-between items-center p-3 text-sm">
          {/* navigate to extensa.agency with an a tag in a new tab */}
          <a
            href="https://extensa.agency"
            target="_blank"
            rel="noopener noreferrer"
            className="text-white bg-black px-4 py-2 rounded-md hover:bg-gray-800"
          >Extensa AI</a>

          {isSupabaseConnected && <AuthButton />}
        </div>
      </nav>
      <div className="flex-1 w-full flex flex-col items-center justify-center">
        <h2 className="text-3xl font-bold text-center">Welcome to your new Nexjs-Supabase Project!</h2>
        <p className="text-lg text-center mt-4">
          Start working with Kevin to build your new project.
        </p>
      </div>
    </div>
  );
}
