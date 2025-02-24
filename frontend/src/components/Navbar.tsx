import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, User } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <Shield className="h-8 w-8 text-pastel-blue" />
              <span className="ml-2 text-xl font-bold text-gray-900">InsureGuard</span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link to="/plans" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900">
                Plans
              </Link>
              <Link to="/compare" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900">
                Compare
              </Link>
              <Link to="/dashboard" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900">
                Dashboard
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/login" className="text-gray-500 hover:text-gray-900">
              Sign in
            </Link>
            <Link
              to="/signup"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-full text-white bg-pastel-blue hover:bg-blue-600 transition-colors duration-200"
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;