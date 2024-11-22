import Scholarship from "./Scholarship";
import Exam from "./Exam";
import "./index.css";

const App = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl m-8 text-center">Prolog Q2 Client</h1>
      <h1 className="text-2xl m-8 text-center">22BCE0511 - Vishnu P K</h1>
      <div className="flex justify-center gap-8">
        <div className="w-full sm:w-1/2 lg:w-1/3">
          <Scholarship />
        </div>
        <div className="w-full sm:w-1/2 lg:w-1/3">
          <Exam />
        </div>
      </div>
    </div>
  );
};

export default App;
